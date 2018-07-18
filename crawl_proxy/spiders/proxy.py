# -*- coding: utf-8 -*-
import scrapy


class ProxySpider(scrapy.Spider):
    name = 'proxy'

    start_urls = [
        'https://free-proxy-list.net',
        'https://www.us-proxy.org/'
    ]

    css_tables = [
        '#proxylisttable',
        '#proxylisttable'
    ]

    def start_requests(self):
        for i, start_url in enumerate(self.start_urls):
            yield scrapy.Request(url=start_url, meta={'css_table': self.css_tables[i]})

    def parse(self, response):
        url = response.request.url

        proxies = set()

        table = response.css(response.request.meta['css_table'])
        rows = table.css('tbody tr')

        print('Url: {} Proxies {}'.format(url, len(rows)))

        for row in rows:
            ip_address = row.css('td:nth-child(1)::text').extract_first()
            port = row.css('td:nth-child(2)::text').extract_first()

            protocol = row.css('td:nth-child(7)::text').extract_first()
            protocol = 'https' if protocol.lower() == 'yes' else 'http'

            proxy = '{}://{}:{}'.format(protocol, ip_address, port)

            proxies.add(proxy)

        yield {
            'url': url,
            'proxies': proxies
        }
