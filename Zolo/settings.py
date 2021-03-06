# -*- coding: utf-8 -*-

import os

from tools.get_sql_con import get_conn

# Scrapy settings for Zolo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Zolo'

SPIDER_MODULES = ['Zolo.spiders']
NEWSPIDER_MODULE = 'Zolo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Zolo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED =True
# DOWNLOAD_DELAY = 5

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Zolo.middlewares.ZoloSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Zolo.middlewares.RandomUserAgentMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    # 'Zolo.middlewares.RandomProxyMiddleware':544,
}
RANDOM_UA_TYPE = "random"

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'Zolo.pipelines.ZoloPipeline': 300,
    'Zolo.pipelines.MarketStatsPipeline1':300,
   #  'Zolo.pipelines.IndexHousePipeline':300,
   #  'Zolo.pipelines.BasedOnProvincePipeline':300,
}
# 配置UserAgent随机是通过那个浏览器产生的；


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# mysql 数据库配置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'zolo'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'

# 日志输出：
LOG_FILE="log.txt"

# city list file path
city_list_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tools/SourceData.csv'


# ssh connect database
is_ssh = True
ssh_host = ""
ssh_port = 22
ssh_username = ""
ssh_password = ""
database = ""
user = "dealtap"
password = "dealtap"
host = "localhost"
port = 5432

# 数据库连接对象和ssh连接服务：
conn, server = get_conn(True)

# 再爬虫开始之前将trend表置空
sql_string_truncate_trend = '''
        TRUNCATE trend
'''
# 向estate_expect_deal_price_params_data_test 插入基本数据
estate_expect_deal_price_params_data_test_insert_base = '''
    INSERT INTO 
    estate_expect_deal_price_params_data_test(city,"provinceCode","citySpLp","provinceSpLp",dom,"listingCount","soldCount","createdDate","floatingValue")
    (select 
    td.city as city,
    nt.province as "provinceCode",
    td.selling_to_listing_price_ratio AS "citySpLp",
    td.selling_to_listing_price_ratio AS "provinceSpLp",
    
    
    td.average_days_on_market AS dom,
    
    td.new_listings AS "listingCount",
    td.homes_sold AS "soldCount",
    td."createdDate",
    2
    
    from trend td
    LEFT JOIN 
    (
    SELECT *
    FROM province_city_map
    ) nt
    ON td.city = nt.city
    ORDER BY "provinceCode"
    )
'''
# 查询出privinceCode，作为循环
get_province_code = '''
    SELECT "provinceCode"
    FROM estate_expect_deal_price_params_data_test
    where
    "createdDate"=date(now())
    AND city!=''
    AND city IS NOT NULL
'''

