# -*- coding:utf8 -*-
import urllib2


class Html_Downloader(object):

    def download(self, url):
        if url is None:
            return None
        response = urllib2.urlopen(url)

        if response.getcode() != 200:
            return None

        return response.read()