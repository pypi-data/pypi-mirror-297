"""

Utils for RSS
"""

from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup
import feedparser
from pydantic import BaseModel
import requests
import dateutil.parser


class RSSSource(BaseModel):
    title: str
    link: str
    avatar_url: Optional[str] = None


def parse_datetime_wisely(date_string):
    """
    尝试解析多种格式的日期时间字符串。
    如果所有尝试都失败，则返回当前时间。
    """
    if not date_string:
        return datetime.now()

    # 首先尝试使用 dateutil 解析
    try:
        return dateutil.parser.parse(date_string)
    except (ValueError, TypeError):
        pass

    # 定义一系列常见的日期时间格式
    formats = [
        "%a, %d %b %Y %H:%M:%S %Z",  # RFC 822
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601
        "%Y-%m-%d %H:%M:%S.%f",  # 带微秒的标准格式
        "%Y-%m-%d %H:%M:%S",  # 标准格式
        "%Y-%m-%d",  # 仅日期
        "%d %b %Y %H:%M:%S %z",  # 另一种常见格式
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    # 如果所有尝试都失败，记录错误并返回当前时间
    print(f"Unable to parse date string: {date_string}")
    return datetime.now()


def extract_img_url_from_html(s):
    soup = BeautifulSoup(s, "html.parser")
    img_tags = soup.find_all("img")
    img_urls = [img["src"] for img in img_tags if "src" in img.attrs]
    if len(img_urls) > 0:
        return img_urls[0]
    else:
        return ""


def get_avatar_url(homepage_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(homepage_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for the favicon link in the head
        favicon_link = soup.find("link", rel="icon") or soup.find(
            "link", rel="shortcut icon"
        )

        if favicon_link and "href" in favicon_link.attrs:
            favicon_url = favicon_link["href"]
            if favicon_url.startswith("//"):
                favicon_url = "http:" + favicon_url
            else:
                if not favicon_url.startswith("http"):
                    # Handle relative URLs
                    favicon_url = requests.compat.urljoin(homepage_url, favicon_url)
            return favicon_url
        else:
            return None
    except Exception as e:
        print(f"获取头像 URL 失败: {e}")
        return None


def get_rss_info(url):
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            # print(f"==> RSS 源 {url} 有效，包含 {len(feed.entries)} 条目")
            # print(f"==> RSS info: {feed.feed}")
            # print(feed.entries[0])
            # save avatar url?
            link = feed.feed.link
            # avatar_url = get_avatar_url(homepage_url)
            avatar_url = get_avatar_url(link)
            print(f"avatar_url: {avatar_url}, url: {url} {link}")
            return RSSSource(
                title=feed.feed.title, link=feed.feed.link, avatar_url=avatar_url
            )
        else:
            print(f"RSS 源 {url} 接通但内容无效")
            return None
    except Exception as e:
        print(f"RSS 源 {url} 接通失败: {e}")
        return None


def check_rss_url_valid(url):
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            print(f"==> RSS 源 {url} 有效，包含 {len(feed.entries)} 条目")
            print(f"==> RSS info: {feed.feed}")
            print(feed.entries[0])
            return True
        else:
            print(f"RSS 源 {url} 接通但内容无效")
            return False
    except Exception as e:
        print(f"RSS 源 {url} 接通失败: {e}")
        return False


"""
https://status.uri.wang/status/rsshub
"""

# rss_url = "i.scnu.edu.cn/sub"
# rss_url = "https://rss.injahow.cn"
rss_url = "http://127.0.0.1:5005"  # default port

default_rss_sources = [
    # f"{rss_url}/apnews/rss/business",
    # f"{rss_url}/pixiv/search/Nezuko/popular",
    # f"{rss_url}/caixinglobal/latest",
    # f"{rss_url}/36kr/hot-list",
    # f"{rss_url}/19lou/jiaxing",
    # f"{rss_url}/aliresearch/information",
    # f"{rss_url}/dedao/list/年度日更",
    # f"{rss_url}/guancha/headline",
    # f"{rss_url}/guancha/",
    # f"{rss_url}/geekpark/breakingnews/",
    # f"{rss_url}/zhihu/hotlist/",
    # f"{rss_url}/guokr/scientific/",
    # f"{rss_url}/cctv/world/",
    # f"{rss_url}/xueqiu/user/6410914956",
    # f"{rss_url}/xueqiu/user/2852344450",
    # f"{rss_url}/kkj/news",
    # f"{rss_url}/huxiu/briefcolumn/1",
    # f"{rss_url}/xinhuanet/yaodianjujiao",
    f"{rss_url}/cls/telegraph",
    f"{rss_url}/tadoku/books/l0",
    f"{rss_url}/infoq/recommend",
    f"{rss_url}/bbwc/realtime/2",
    f"{rss_url}/zhihu/daily",
    f"{rss_url}/gscore/rss",
    f"{rss_url}/ruanyifeng/rss",
    # f"{rss_url}/36kr/rss",
    f"{rss_url}/taimeiti/rss",
    f"{rss_url}/huxiu/rss",
    f"{rss_url}/geekpark/rss",
]
