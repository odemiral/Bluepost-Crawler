from scrapy.item import Item, Field

'''
Class that holds all the necessary data required from a blue post.
'''


class BluePost(Item):
    content = Field()
    url = Field()
    author = Field()
    date = Field()
    forum = Field()
    title = Field()

