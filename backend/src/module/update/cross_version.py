import re

from urllib3.util import parse_url

from module.network import RequestContent
from module.rss import RSSEngine
from module.utils import save_image


def from_30_to_31():
    with RSSEngine() as db:
        db.migrate()
        # Update poster link
        bangumis = db.bangumi.search_all()
        rss_pool = []
        for bangumi in bangumis:
            if bangumi.poster_link:
                rss_link = bangumi.rss_link.split(",")[-1]
                if rss_link not in rss_pool and not re.search(
                    r"\d+.\d+.\d+.\d+", rss_link
                ):
                    rss_pool.append(rss_link)
                root_path = parse_url(rss_link).host
                if "://" not in bangumi.poster_link:
                    bangumi.poster_link = f"https://{root_path}{bangumi.poster_link}"
        db.bangumi.update_all(bangumis)
        for rss in rss_pool:
            if "mybangumi" in rss.lower():
                aggregate = True
            else:
                aggregate = False
            db.add_rss(rss_link=rss, aggregate=aggregate)


def cache_image():
    with RSSEngine() as db, RequestContent() as req:
        bangumis = db.bangumi.search_all()
        for bangumi in bangumis:
            if bangumi.poster_link:
                # Hash local path
                img = req.get_content(bangumi.poster_link)
                suffix = bangumi.poster_link.split(".")[-1]
                img_path = save_image(img, suffix)
                bangumi.poster_link = img_path
        db.bangumi.update_all(bangumis)
