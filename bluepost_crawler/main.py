from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from spiders.diablo_spider import DiabloSpider
from spiders.starcraft_spider import StarCraftSpider
from spiders.wow_spider import WoWSpider
from spiders.heartstone_spider import HearthStoneSpider
from spiders.hots_spider import HoTSSpider

from spiders.configuration import Configuration



'''
reactor.stop only when ALL the spiders are finish
use a counter to check if all the spiders are finished before stopping reactor.
'''

'''
@args[0] = spider
@args[1] = settings
'''
def runSpider(args):
    spider = args[0]
    settings = args[1]
    crawler = Crawler(settings)
    crawler.signals.connect(stopCrawler, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


'''
return spider objects in a list.
'''
def getSpiderObjects(config):
    spiders = []
    spiders.append(DiabloSpider(config))
    spiders.append(StarCraftSpider(config))
    spiders.append(WoWSpider(config))
    spiders.append(HearthStoneSpider(config))
    spiders.append(HoTSSpider(config))
    return spiders

'''
static var to help stopping the reactor.
'''
runSpider.counter = 5


'''
When a crawler finishes it calls this function, when all crawlers are finished this function stops the reactor.
'''
def stopCrawler():
    runSpider.counter -= 1
    if runSpider.counter == 0:
        reactor.stop()
    print 'active crawlers: ' + str(runSpider.counter)
    #return activeCrawler


'''
Run Spiders in a single thread
NOTE: network operations are still asynchronous, so there is no benefit for using multithreads
'''
def sequentialCrawling():
    config = Configuration()
    spiders = getSpiderObjects(config)
    settings = get_project_settings()
    for spider in spiders:
        args = [spider, settings]
        runSpider(args)
    log.start()
    reactor.run() # the script will block here until the spider_closed signal was sent

def main():
    sequentialCrawling()

if __name__ == '__main__':
    main()
