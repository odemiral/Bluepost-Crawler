'''
Scrapy settings for BluePost project.
More info about settings can be found:  http://doc.scrapy.org/en/latest/topics/settings.html
'''

import os

BOT_NAME = 'bluepost_crawler'

SPIDER_MODULES = ['bluepost_crawler.spiders']
NEWSPIDER_MODULE = 'bluepost_crawler.spiders'

DEFAULT_ITEM_CLASS = 'bluepost_crawler.items.BluePost'

ITEM_PIPELINES = {'bluepost_crawler.pipelines.BluePostPipeline': 1,
                  'bluepost_crawler.pipelines.textPipeline': 2}

#COOKIES_ENABLED = 0