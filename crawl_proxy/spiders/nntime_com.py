# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
from crawl_proxy.custom_settings import custom_settings

lua_code = """
function main(splash)
  local url = splash.args.url
  assert(splash:go(url))
  assert(splash:wait(0.5))
  return {
    html = splash:html(),
  }
end
"""


class NntimeComSpider(scrapy.Spider):
    name = 'nntime.com'

    start_urls = ['http://nntime.com/proxy-list-01.htm']

    custom_settings = custom_settings

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy_splash.SplashRequest(url, args={'lua_source': lua_code}, endpoint='execute')

    def parse(self, response):
        nav = response.css('#navigation a')[-1]

        if nav.css('a::text').extract_first() == 'next':
            next_page = nav.css('a::attr(href)').extract_first()
            next_page = response.urljoin(next_page)

            # yield scrapy_splash.SplashRequest(next_page)

        url = response.request.url

        proxies = set()

        table = response.css('#proxylist')
        rows = table.css('tr')

        for row in rows:
            ip_address = row.css('td:nth-child(2)::text').extract_first()
            if ip_address is not None:
                protocol = 'http'

                proxy = '{}://{}'.format(protocol, ip_address)

                proxies.add(proxy)

        yield {
            'url': url,
            'proxies': proxies,
            'p_count': len(proxies)
        }
