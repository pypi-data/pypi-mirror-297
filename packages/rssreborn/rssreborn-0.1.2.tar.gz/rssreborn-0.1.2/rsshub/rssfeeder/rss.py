"""

Automatically upate RSS Hub


- roll_in_rss: function get url, check_rss_url_valid if valid, store it into sqlite, using sqlachemy
- get_rss_content_periodically: 3 h , very 3 hours check new contents from all RSS urls in sql, save new contents into sqlit using sqlachedmy
- gen_new_content_summary: using Ai function get_summary to get summary of each new content, and using ai function get_labels to get labels for content, and labels save to sql
- get_new_articles: serving get the latest new articles, with the lastId from server side, return from lastId -> latestId contents.

"""

from concurrent.futures import ThreadPoolExecutor
import threading
import time
import os
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
from apscheduler.schedulers.background import BackgroundScheduler
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

news_agent = NewsAgent()


def roll_in_rss(url):
    if check_rss_url_valid(url):
        feed = RSSFeed(url=url)
        session.add(feed)
        session.commit()


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
            for entry in feed.entries:
                # Check if the article already exists in the database
                existing_feed = (
                    session.query(RSSFeed)
                    .filter(
                        or_(
                            RSSFeed.url == entry.link,
                            RSSFeed.title.like(f"%{entry.title}%"),
                        )
                    )
                    .first()
                    # .filter(RSSFeed.url == entry.link).first()
                )
                # existing_feed = None
                if not existing_feed:
                    try:
                        new_feed = RSSFeed(
                            url=entry.link,
                            title=entry.title,
                            content=(
                                entry.summary_detail.value
                                if "summary_detail" in entry
                                else entry.description
                            ),
                            summary=(
                                entry.summary
                                if "summary" in entry
                                else entry.description
                            ),
                            source_name=source.name,
                            source_url=source.url,
                            source_avatar_url=source.avatar_url,
                            hero_img_url=extract_img_url_from_html(entry.summary),
                            published=(
                                parse_datetime_wisely(entry.published)
                                if hasattr(entry, "published")
                                else datetime.now()
                            ),
                            created=datetime.now(),
                            author=entry.author if hasattr(entry, "author") else None,
                        )
                    except Exception as e:
                        import traceback

                        logger.error(f"got error: {e}")
                        logger.error(f"got error: {traceback.print_exc()}")
                        continue
                    session.add(new_feed)
                    session.commit()  # Commit here to ensure the new feed has an ID

                    new_feed.ai_summary = news_agent.get_summary(new_feed.content)
                    new_feed.tags = news_agent.get_tags(new_feed.content)
                    # new_feed.ai_summary = ""
                    # new_feed.tags = ""
                    session.commit()

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
                else:
                    pass
                    # logger.info(f"{existing_feed} already exist.")
        else:
            logger.error(f"request url error: {source.url}")


def save_rss_source(rss_url):
    info = get_rss_info(rss_url)
    if info is not None:
        existing_source = session.query(RSSSource).filter_by(url=rss_url).first()
        # logger.info(existing_source)
        if existing_source is None:
            new_source = RSSSource(
                url=rss_url, name=info.title, avatar_url=info.avatar_url, link=info.link
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


def start_feeds_scheduler():
    save_thread = threading.Thread(target=save_rss_url_work)
    save_thread.start()

    def run_client(client):
        client.run_forever()

    def run_scheduler():
        # executor = ThreadPoolExecutor(max_workers=1)
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            update_rss_content_and_generate_summary,
            "interval",
            minutes=5,
            max_instances=1,
        )
        scheduler.add_job(
            lambda: logger.info("Scheduler is still running"), "interval", minutes=1
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
