from battlenet_spider import BnetSpider


class StarCraftSpider(BnetSpider):

    name = "StarCraft II"
    def __init__(self, config, category=None, *args, **kwargs):
        super(StarCraftSpider, self).__init__(config)
        self.start_urls = [self.config.bnet_sc2_url]
        print 'url: ' + str(self.start_urls)


