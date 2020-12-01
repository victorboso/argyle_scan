BOT_NAME = 'scan'

SPIDER_MODULES = ['scan.spiders']
NEWSPIDER_MODULE = 'scan.spiders'

ROBOTSTXT_OBEY = False

COOKIES_ENABLED = True
COOKIES_DEBUG = True
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
FEED_EXPORT_ENCODING = 'utf-8'
SPLASH_URL = 'http://localhost:8050'
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 401
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPLASH_COOKIES_DEBUG = True
USER_AGENT_LIST = "your path to [user_agent_file.txt]"
# EX: USER_AGENT_LIST = "/Users/victorboso/Documents/dev/argyle/web_scraping/scan/scan/user_agent_list.txt"