

class Configuration(object):
    def __init__(self):

        #TODO: parse .us and en separately to give users option to change language and location.
        self.bnet_diablo_url = 'http://us.battle.net/d3/en/forum/blizztracker/'
        self.bnet_sc2_url = 'http://us.battle.net/sc2/en/forum/blizztracker/'
        self.bnet_wow_url = 'http://us.battle.net/wow/en/forum/blizztracker/'
        self.bnet_hots_url = 'http://us.battle.net/heroes/en/forum/blizztracker/'
        self.bnet_hearthstone_url = 'http://us.battle.net/hearthstone/en/forum/blizztracker/'

        self.bnet_US = 'http://us.battle.net'