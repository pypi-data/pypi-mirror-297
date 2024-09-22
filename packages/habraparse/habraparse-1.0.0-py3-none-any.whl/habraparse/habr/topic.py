
from logging import debug, info
from copy import deepcopy

class PostDeleted(Exception):
    pass

class HabraTopic:

    def __init__(self):
        self.post = {}

    def author(self):
        return deepcopy(self.post['author'])
###
    def author_url(self):
        return deepcopy(self.post['author_url'])

    def desc(self):
        return deepcopy(self.post['desc'])

    def styles(self):
        return deepcopy(self.post['styles'])

###
    def text(self):
        return deepcopy(self.post['text'])

    def title(self):
        return deepcopy(self.post['title'])

    def rating(self):
        return deepcopy(self.post['rating'])

    def comments(self):
        return deepcopy(self.post['comments'])

    def comments_count(self):
        return deepcopy(self.post['comments_count'])

    def post_id(self):
        return self._topic_id
