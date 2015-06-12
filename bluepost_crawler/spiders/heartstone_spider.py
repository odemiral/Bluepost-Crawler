from battlenet_spider import BnetSpider


class HearthStoneSpider(BnetSpider):

    name = "HearthStone"
    def __init__(self, config, category=None, *args, **kwargs):
        super(HearthStoneSpider, self).__init__(config)
        self.start_urls = [self.config.bnet_hearthstone_url]
        print 'url: ' + str(self.start_urls)
