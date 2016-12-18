import os
import urllib
import requests
import re
from lxml import etree as etree
from bdl.item import Item
from bdl.exceptions import *
import bdl.downloaders
import bdl.engine


class Engine(bdl.engine.Engine):

    # =========================================================================
    # BDL ENGINE API
    # =========================================================================

    @staticmethod
    def get_repo_name(url, **kwargs):
        req = requests.get(url)
        tree = etree.fromstring(req.text, parser=etree.HTMLParser())
        return tree.xpath(".//*/span[@class='subject']")[0].text

    @staticmethod
    def is_reachable(url, **kwargs):
        return requests.get(url).ok

    def __init__(self, url, config, progress):
        super().__init__(url, config, progress)

    def pre_connect(self, **kwargs):
        paths = urllib.parse.urlparse(self.url).path[1:].split('/')
        self.config["name"] = self.get_repo_name(self.url, **kwargs)
        self.config["section"] = paths[0]
        self.config["identifier"] = paths[-1].split('.')[0]

    def pre_update(self, **kwargs):
        pass

    def count_all(self, **kwargs):
        return len(self.list_files(self.url))

    def count_new(self, last_item, last_position, **kwargs):
        return len(self.list_files(self.url)[last_position:])

    def update_all(self, **kwargs):
        for item in self.update_new(None, 0, **kwargs):
            yield item

    def update_new(self, last_item, last_position, **kwargs):
        results = self.list_files(self.url)[last_position:]
        session = requests.Session()
        if len(results) > 0:
            for post_id, item_url in results:
                item = [i for i in bdl.downloaders.generic([item_url, ], progress=self.progress, session=session)][0]
                self.set_item_metadata(item, post_id)
                yield item

    def update_selection(self, urls, **kwargs):
        for item in bdl.downloaders.generic(urls, progress=self.progress):
            self.set_item_metadata(item, None)
            yield item

    # =========================================================================
    # ENGINE-SPECIFIC
    # =========================================================================

    def set_item_metadata(self, item, post_id=None):
        """Set an item's metadata.
        """
        item.set_metadata({"thread_section": self.config["section"],
                           "thread_name": self.config["name"],
                           "thread_id": self.config["identifier"],
                           "post_id": post_id})

    def list_files(self, url):
        """Returns the files URL.
        """
        rep = requests.get(url)
        if not rep.ok:
            raise EngineNetworkError(
                self.name, "{}: {}".format(rep.status_code, rep.reason))
        tree = etree.fromstring(rep.text, etree.HTMLParser())
        results = []
        # First, list all posts with files.
        for post in tree.xpath(".//div[contains(@class, 'has-file')]"):
            # Extract all posts' images and yield a tuple with (post_id, image_url)
            for link in post.xpath(".//div[@class='files']//div[contains(@class, 'file')]//a[@target='_blank']"):
                results.append((post.attrib["id"], link.attrib["href"]))
        return results
