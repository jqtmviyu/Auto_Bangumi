import os.path
import re

import requests
from bs4 import BeautifulSoup
import logging

from conf import settings
from network.request import RequestsURL

logger = logging.getLogger(__name__)


class FullSeasonGet:
    def __init__(self, group, bangumi_name, season, sub, source, dpi , request: RequestsURL):
        self.bangumi_name = re.sub(settings.rule_name_re, " ", bangumi_name).strip()
        self.group = "" if group is None else group
        self.season = season
        self.subtitle = "" if sub is None else sub
        self.source = "" if source is None else source
        self.dpi = dpi
        self._req = request

    def get_season_rss(self):
        if self.season == "S01":
            season = ""
        else:
            season = self.season
        search_str = re.sub(r"[\W_]", "+",
                            f"{self.group} {self.bangumi_name} {season} {self.subtitle} {self.source} {self.dpi}")
        season = self._req.get_url(search_str)
        torrents = season.find_all("enclosure")
        return torrents

    def add_torrents_info(self):
        torrents = self.get_season_rss()
        downloads = []
        for torrent in torrents:
            download_info = {
                "url": torrent["url"],
                "save_path": os.path.join(
                        settings.download_path,
                        self.bangumi_name,
                        self.season)
            }
            downloads.append(download_info)
        return downloads

