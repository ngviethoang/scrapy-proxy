# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
from crawl_proxy.custom_settings import custom_settings


class GatherproxyComSpider(scrapy.Spider):
    name = 'gatherproxy.com'

    start_urls = [
        'http://www.gatherproxy.com/proxylist/anonymity'
    ]

    anonymity_types = [
        'elite',
        'anonymous',
        'transparent'
    ]

    custom_settings = custom_settings

    def start_requests(self):
        for url in self.start_urls:
            for anonymity_type in self.anonymity_types:
                formdata = {'Type': anonymity_type, 'PageIdx': '1'}

                yield scrapy_splash.SplashFormRequest(url=url, formdata=formdata, meta={'formdata': formdata})

    def parse(self, response):
        url = response.url

        formdata = response.request.meta['formdata']

        proxies = set()

        table = response.css('#tblproxy')
        rows = table.css('tr')

        print('Url: {} Proxies {} formdata {}'.format(url, len(rows), formdata))

        for row in rows:
            ip_address = row.css('td:nth-child(2)::text').extract_first()
            if ip_address is not None:
                port = row.css('td:nth-child(3)::text').extract_first()
                protocol = 'http'

                proxy = '{}://{}:{}'.format(protocol, ip_address, port)

                proxies.add(proxy)

        # get next page
        next_page = response.css('.pagenavi .current + a::text').extract_first()
        if next_page is not None:
            formdata['PageIdx'] = next_page

            yield scrapy_splash.SplashFormRequest(url=url, formdata=formdata, meta={'formdata': formdata})

        yield {
            'url': url,
            'proxies': proxies,
            'p_count': len(proxies),
            'type': formdata['Type']
        }
