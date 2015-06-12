import sys

from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from bluepost_crawler.items import BluePost



'''
This is the base class for all the other spiders.
Bnet uses similar conventions which makes the crawling rules for each spider almost the same (except for diablo forums).
Just like any other scrapy spiders, it inherits from CrawlSpider
'''


'''
TODO: MAKE SURE IT VISITS THE SAME LINK MULTIPLE TIMES (WITH DIFFERENT FRAG IDS)
'''
class BnetSpider(CrawlSpider):
    def __init__(self, config, category=None, *args, **kwargs):
       super(BnetSpider, self).__init__(*args, **kwargs)
       self.config = config

       '''
       Configure all the hardcoded xpaths queries.
       '''
       self.urlXpath = 'td[@class="title-cell"]/div[@class="content"]/a/@href'
       self.authorXpath = 'td[@class="author-cell"]/span[@class="author-wrapper"]/span[@class="author-name blizzard-post"]/text()'
       self.titleXpath = 'td[@class="title-cell"]/div[@class="desc"]/a[@class="forum-topic"]/text()'
       self.forumXpath = 'td[@class="title-cell"]/div[@class="desc"]/a[@class="forum-source"]/text()'
       self.contentXpath = 'div[@class="post-content"]/div[@class="post-detail"]'
       self.dateXpath = 'div[@class="post-info"]/div[@class="post-info-wrapper"]/div[@class="date"]/@data-tooltip'

       #Parent Xpath Queries for all the other xpath queries
       self.totalPostsParentXpath = '//div'
       self.blizzTrackParentXpath = '//tr'

       #This query is used to find the post with correct fragment identifier
       self.relaventPostXPath = 'div[@class="post-info"]/div[@class="post-info-wrapper"]/a[@href="%s"]/@href'

    '''
    Calls the url to the actual post and extracts the full text content.
    Response should have the data we need.

    create a response from a url then use selector to get necessary info.
    '''
    def extractContent(self, response, fragmentId):
        item = BluePost()
        item['forum'] = response.meta['forum']
        item['title'] = response.meta['title']
        item['author'] = response.meta['author']

        sel = Selector(response=response)
        totalCellPosts = sel.xpath(self.totalPostsParentXpath)
        #sys.stderr.write('totalCellPosts Length: %s \n' % str(len(totalCellPosts)))

        #xpathQuery that finds the post that matches the fragment identifier.
        xpathQuery = self.relaventPostXPath % ('#' + str(fragmentId))

        '''
        This is wildly inefficient!
        once you find xPathQuery, no need to iterate over all the post there's gotta be only 1 post with xpath query.
        '''
        for post in totalCellPosts:
            relaventPost = post.xpath(xpathQuery).extract()
            #There is only 1 relatventPost, after you find it, return the item to item pipeline.
            if relaventPost:
                content = post.xpath(self.contentXpath).extract()
                date = post.xpath(self.dateXpath).extract()
                item['date'] = date
                item['content'] = content
                #break

                '''
                This will obv cause a crash when relaventPost is not in totalCellPosts(content, date undefined)
                '''
                #sys.stderr.write("___Crawling for this page is over! Results___ \n")
                #sys.stderr.write("Forum: %s \n" % str(item['forum']))
                #sys.stderr.write("title: %s \n" % str(item['title']))
                #sys.stderr.write("author: %s \n" % str(item['author']))
                #sys.stderr.write("content: %s \n" % str(item['content']))
                #sys.stderr.write("date: %s \n" % str(item['date']))
                return item



    def parse(self, response):
        sys.stderr.write('Response URL: %s \n' % str(response.url))

        sel = Selector(response)
        totalCellPosts = sel.xpath(self.blizzTrackParentXpath)

        #testing = sel.xpath('//ul[@class="ui-pagination"]/li[@class="cap-item"]/a[@class="page-next"]/@href').extract()
        #sys.stderr.write("Next Page: %s \n" % str(testing))

        #Skip the first one (will be empty)
        iterPosts = iter(totalCellPosts)
        next(iterPosts)

        for post in iterPosts:
            item = BluePost()
            item['url'] = self.config.bnet_US + post.xpath(self.urlXpath).extract()[0]

            #Check if the link contains fragment identifier (It has to have one!)
            try:
                fragmentId = item['url'].split('#')[1]
            except IndexError as e:
                sys.stderr.write("Cannot parse link! It doesn't contain a fragment identifier! \n")
                continue

            '''
            Partially populate requests meta which will be used to construct an item in Item Pipeline.
            Note: lambda callback is used to send fragmentId as an argument to the callback function.
            No other lambda wizardry is performed (I Promise!)
            '''
            request =  Request(url=item['url'], callback=lambda l, fragmentId=fragmentId:self.extractContent(l, fragmentId))
            request.meta['forum'] = post.xpath(self.forumXpath).extract()
            request.meta['title'] = post.xpath(self.titleXpath).extract()
            request.meta['author'] = post.xpath(self.authorXpath).extract()
            yield request

        '''
        Once all the posts in a page are crawled, move on to the next page and yield another request until no more pages left to crawl.
        '''
        nextPageURL = sel.xpath('//ul[@class="ui-pagination"]/li[@class="cap-item"]/a[@class="page-next"]/@href').extract()
        if nextPageURL:
            nextPageURL = self.start_urls[0] + nextPageURL[0]
            sys.stdout.write("Next Page: %s \n" % str(nextPageURL))
            yield Request(url=nextPageURL, callback=self.parse)
        else:
            sys.stderr.write('Last Page! \n')

