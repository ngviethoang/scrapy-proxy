# -*- coding: utf-8 -*-
""" Run spiders to get proxies """

from scrapy.crawler import CrawlerProcess
from crawl_proxy.spiders.gatherproxy_com import GatherproxyComSpider
from crawl_proxy.spiders.nntime_com import NntimeComSpider
from crawl_proxy.spiders.proxylist_me import ProxylistMeSpider
from datetime import datetime


if __name__ == '__main__':
    start = datetime.now()

    process = CrawlerProcess()
    process.crawl(GatherproxyComSpider)
    process.crawl(ProxylistMeSpider)
    # process.crawl(NntimeComSpider)  # removed
    process.start()

    stop = datetime.now()
    runtime = stop - start
    print('Runtime: {}'.format(runtime))
