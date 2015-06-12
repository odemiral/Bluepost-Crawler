from battlenet_spider import BnetSpider


class WoWSpider(BnetSpider):

    name = "WoW"
    def __init__(self, config, category=None, *args, **kwargs):
        super(WoWSpider, self).__init__(config)
        self.start_urls = [self.config.bnet_wow_url]
        print 'url: ' + str(self.start_urls)
