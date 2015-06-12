from battlenet_spider import BnetSpider

class DiabloSpider(BnetSpider):

    name = "DiabloIII"
    def __init__(self, config, category=None, *args, **kwargs):
        super(DiabloSpider, self).__init__(config)
        self.start_urls = [self.config.bnet_diablo_url]
        print 'url: ' + str(self.start_urls)

        self.contentXpath = 'td/div[@class="post-detail"]'
        self.dateXpath = 'td[@class="post-info"]/div[@class="post-info-wrapper"]/div[@class="date"]/@data-tooltip'
        self.totalPostsParentXpath = '//tr'
        self.relaventPostXPath = 'td[@class="post-info"]/div[@class="post-info-wrapper"]/a[@href="%s"]/@href'