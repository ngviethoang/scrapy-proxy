splash_settings = {
    'SPLASH_URL': 'http://localhost:8050',

    'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',

    'SPIDER_MIDDLEWARES': {
       'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    },

    'DOWNLOADER_MIDDLEWARES': {
       'scrapy_splash.SplashCookiesMiddleware': 723,
       'scrapy_splash.SplashMiddleware': 725,
       'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
       'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    }
}

mongo_settings = {
    'URI': 'mongodb://localhost:27017',
    'DATABASE': 'amazon',

    'PROXIES_COLLECTION': 'proxies',

    'ITEM_PIPELINES': {
       'crawl_proxy.pipelines.MongoPipeline': 302
    }
}

mysql_settings = {
    "MYSQL_HOST": "45.79.107.74",
    "MYSQL_USER": "pec91p_t33_es",
    "MYSQL_PASSWD": "gLwHfkoeN6C0WBx",
    "MYSQL_DB": "pec91p_t33_es"
}

custom_settings = dict(splash_settings, **mongo_settings, **mysql_settings)
