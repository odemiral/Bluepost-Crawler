from battlenet_spider import BnetSpider


class HoTSSpider(BnetSpider):

    name = "HoTS"
    def __init__(self, config, category=None, *args, **kwargs):
        super(HoTSSpider, self).__init__(config)
        self.start_urls = [self.config.bnet_hots_url]
        print 'url: ' + str(self.start_urls)