# -*- coding: utf-8 -*-
""" Run spiders to get proxies """

from scrapy.crawler import CrawlerProcess
from crawl_proxy.spiders.proxylist_me import ProxylistMeSpider
from crawl_proxy.spiders.gatherproxy_com import GatherproxyComSpider
from crawl_proxy.spiders.nntime_com import NntimeComSpider


if __name__ == '__main__':
    process = CrawlerProcess()
    # process.crawl(ProxylistMeSpider)
    process.crawl(GatherproxyComSpider)  # need to run scrapy splash
    # process.crawl(NntimeComSpider)  # removed
    process.start()
