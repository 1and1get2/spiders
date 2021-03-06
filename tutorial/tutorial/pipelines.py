# -*- coding: utf-8 -*-
import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('./data/douban/book.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
