#!/usr/bin/python

from scrapy.cmdline import execute

execute("scrapy crawl coser -o item.json".split())
