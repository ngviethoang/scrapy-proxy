# -*- coding: utf-8 -*-
import scrapy


class ProxylistMeSpider(scrapy.Spider):
    name = 'proxylist.me'

    start_urls = ['https://proxylist.me']

    def parse(self, response):
        next_page = response.css('.pagination li.active + li a::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)

            yield scrapy.Request(url=next_page)

        url = response.request.url

        proxies = set()

        table = response.css('#datatable-row-highlight')
        rows = table.css('tbody tr')

        print('Url: {} Proxies {}'.format(url, len(rows)))

        for row in rows:
            ip_address = row.css('td:first-child a::text').extract_first()
            if ip_address is not None:
                port = row.css('td:nth-child(2)::text').extract_first()
                protocol = 'http'

                proxy = '{}://{}:{}'.format(protocol, ip_address, port)

                proxies.add(proxy)

        yield {
            'url': url,
            'proxies': proxies,
            'p_count': len(proxies)
        }
