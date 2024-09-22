"""

Automatically upate RSS Hub


- roll_in_rss: function get url, check_rss_url_valid if valid, store it into sqlite, using sqlachemy
- get_rss_content_periodically: 3 h , very 3 hours check new contents from all RSS urls in sql, save new contents into sqlit using sqlachedmy
- gen_new_content_summary: using Ai function get_summary to get summary of each new content, and using ai function get_labels to get labels for content, and labels save to sql
- get_new_articles: serving get the latest new articles, with the lastId from server side, return from lastId -> latestId contents.

"""

from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from sqlite3 import IntegrityError
import threading
import time
import os
import uuid
from fastapi import HTTPException
import requests
from sqlalchemy import or_
from .store.dbs import RSSFeed, RSSSource, session
from .utils import (
    check_rss_url_valid,
    extract_img_url_from_html,
    get_rss_info,
    parse_datetime_wisely,
)

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler import CoalescePolicy
import feedparser
from .utils import default_rss_sources
from loguru import logger
from datetime import datetime
from uranuspy.im.client import ChatClient, run_client_forever
from .ai import NewsAgent


uranus_id = os.environ["uranus_id"]
uranus_pwd = os.environ["uranus_pwd"]
assert uranus_id is not None and uranus_pwd is not None, "env need set"
client_uranus = ChatClient(uranus_id, uranus_pwd, broker_address="g.manaai.cn")
# client_uranus = ChatClient(uranus_id, uranus_pwd)

news_agent = NewsAgent()


def roll_in_rss(url):
    if check_rss_url_valid(url):
        feed = RSSFeed(url=url)
        session.add(feed)
        session.commit()


global_lock = threading.Lock()


def update_rss_content_and_generate_summary():
    sources = session.query(RSSSource).all()
    logger.info(f"{len(sources)} sources to go.")
    # logger.info(sources)
    for i, source in enumerate(sources):
        logger.info(f"resolving: {source.name}, {i}")
        response = requests.get(source.url)
        if response.status_code == 200:
            # Parse the RSS feed content
            feed = feedparser.parse(response.text)
            logger.info(f"feed entries: {len(feed.entries)}")
            new_feed_count = 0
            for entry in feed.entries:
                # logger.info(f"entry: {entry.title}")
                # Check if the article already exists in the database
                existing_feed = (
                    session.query(RSSFeed)
                    .filter(
                        or_(
                            RSSFeed.url == entry.link,
                            RSSFeed.url == entry.id,
                            RSSFeed.title.like(f"%{entry.title}%"),
                        )
                    )
                    .first()
                    # .filter(RSSFeed.url == entry.link).first()
                )
                # existing_feed = None
                if existing_feed is None:
                    logger.info(f"entry: {entry.title}")
                    # try:
                    # logger.info(existing_feed)
                    # print(entry)
                    try:
                        new_feed = RSSFeed(
                            url=entry.link,
                            title=entry.title,
                            content=(
                                entry.summary_detail.value
                                if "summary_detail" in entry
                                else (
                                    entry.summary
                                    if "summary" in entry
                                    else (
                                        entry.description
                                        if "description" in entry
                                        else ""
                                    )
                                )
                            ),
                            summary=(
                                entry.summary if "summary" in entry else entry.title
                            ),
                            source_name=source.name,
                            source_url=source.url,
                            source_avatar_url=source.avatar_url,
                            hero_img_url=extract_img_url_from_html(
                                entry.summary if "summary" in entry else ""
                            ),
                            published=(
                                parse_datetime_wisely(entry.published)
                                if hasattr(entry, "published")
                                else datetime.now()
                            ),
                            created=datetime.now(),
                            author=entry.author if hasattr(entry, "author") else None,
                            uuid=str(uuid.uuid4()),
                        )
                    except Exception as e:
                        print(f"fuck you!??? {e}")

                    new_feed_count += 1
                    # print(new_feed_count)
                    try:
                        # print(f"fuck=====? {new_feed.content}")
                        new_feed.ai_summary = news_agent.get_summary(new_feed.content)
                        new_feed.tags = news_agent.get_tags(new_feed.content)
                    except Exception as e:
                        print(e)
                        new_feed.ai_summary = ""
                        new_feed.tags = ""
                    # new_feed.ai_summary = ""
                    # new_feed.tags = ""
                    # print(new_feed.to_json())

                    logger.info(
                        f"new rss: {new_feed.title} {new_feed.published} {new_feed.author} added."
                    )
                    # broadcast to all uranus users
                    msg_to_send = new_feed.to_json()
                    try:
                        client_uranus.send_rss_news_msg_to_room(
                            msg_to_send, "rss/news_all"
                        )
                    except Exception as e:
                        logger.error(f"sending message error: {e}")

                    # wait for sql response
                    time.sleep(1)
                    try:
                        global_lock.acquire()
                        session.merge(new_feed)
                        session.commit()
                        print("saved.")
                        global_lock.release()
                    except IntegrityError as e:
                        session.rollback()
                        print(f"IntegrityError: {e}")
                    except Exception as e:
                        if global_lock.locked():
                            global_lock.release()
                        print(e)
                        continue
                else:

                    # pass
                    logger.info(f"{existing_feed} already exist.")
            logger.info(f"==> save {new_feed_count} new feeds.")
        else:
            logger.error(f"request url error: {source.url}")
    return


def save_rss_source(
    rss_url,
    creator="",
    creator_url="",
):
    info = get_rss_info(rss_url)
    if info is not None:
        existing_source = session.query(RSSSource).filter_by(url=rss_url).first()
        # logger.info(existing_source)
        if existing_source is None:
            new_source = RSSSource(
                url=rss_url,
                name=info.title,
                avatar_url=info.avatar_url,
                link=info.link,
                created=datetime.now(),
                creator=creator,
                creator_url=creator_url,
            )
            session.add(new_source)
            session.commit()
        else:
            existing_source.name = info.title
            existing_source.avatar_url = info.avatar_url
            existing_source.link = info.link
            session.commit()
        return True
    else:
        return False


async def upload_rss_source(request):
    data = await request.json()
    url = data.get("url")
    name = data.get("name")
    avatar_url = data.get("avatar_url")

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Check if the URL is a valid RSS feed
    try:
        response = requests.get(url)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        if not feed.entries:
            raise HTTPException(status_code=400, detail="Invalid RSS feed")
    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Check if the RSS source already exists
    existing_source = session.query(RSSSource).filter_by(url=url).first()
    if existing_source:
        raise HTTPException(status_code=400, detail="RSS source already exists")

    # Create a new RSS source
    new_source = RSSSource(url=url, name=name, avatar_url=avatar_url)
    session.add(new_source)
    session.commit()
    return {"message": "RSS source uploaded successfully", "id": new_source.id}


def save_default_rss_urls():
    for i in default_rss_sources:
        save_rss_source(i)
    logger.info("default rss url initiated.")

    # t1 = run_client_forever(client_uranus)

    # executor = ThreadPoolExecutor(max_workers=1)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     lambda: executor.submit(update_rss_content_and_generate_summary),
    #     "interval",
    #     minutes=5,
    # )
    # scheduler.start()
    # t1.join()


def save_rss_url_work():
    print("sleep 60 seconds wait for server up")
    time.sleep(30)
    logger.info("starting scheduler for feeds?")
    save_default_rss_urls()
    logger.info("saved rss urls.")


def start_feeds_scheduler2():
    save_thread = threading.Thread(target=save_rss_url_work)
    save_thread.start()

    def run_client(client):
        client.run_forever()

    def run_scheduler():
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            update_rss_content_and_generate_summary,
            "interval",
            minutes=2,
            max_instances=1,
        )
        scheduler.add_job(
            lambda: logger.info("Scheduler is still running"), "interval", minutes=2
        )
        scheduler.start()
        return scheduler

    save_thread.join()

    scheduler = run_scheduler()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_client, client_uranus)
        time.sleep(5)
        executor.shutdown(wait=False)
    return scheduler


def start_feeds_scheduler():
    save_thread = threading.Thread(target=save_rss_url_work)
    save_thread.start()
    save_thread.join()

    def run_client(client):
        client.run_forever()

    executor = ThreadPoolExecutor(max_workers=2)
    executor.submit(run_client, client_uranus)

    scheduler = Scheduler()
    scheduler.add_schedule(
        func_or_task_id=update_rss_content_and_generate_summary,
        trigger=IntervalTrigger(minutes=1),
        max_running_jobs=1,
        coalesce=CoalescePolicy.earliest,
    )
    # scheduler.add_schedule(
    #     func_or_task_id=lambda: logger.info("Scheduler is still running"),
    #     trigger=IntervalTrigger(minutes=1),
    # )
    scheduler.start_in_background()

    return scheduler, executor
