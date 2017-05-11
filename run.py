#!/usr/bin/python

from scrapy.cmdline import execute

execute("scrapy crawl coser2 -o item.json".split())
