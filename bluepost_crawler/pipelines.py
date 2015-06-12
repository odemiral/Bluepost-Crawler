from scrapy.settings import CrawlerSettings
from scrapy import log


class BluePostPipeline(object):
    def process_item(self, item, spider):
        return item


class textPipeline(object):
    def process_item(self, item, spider):
        fileName = spider.name + str('.txt')
        with open(fileName, 'a') as txtFile:
            txtFile.write(str(item) + '\n')
'''
if you want to put the actual results to your db this is where you create a pipeline to db.
There are numerous examples online for various db engines
here's one for mongodb: https://realpython.com/blog/python/web-scraping-with-scrapy-and-mongodb/
'''

