#!/usr/bin/env python
# filename: crawl.py
# Run this module using command "python crawl.py"
'''This module is used to crawing the web pages and 
build index for all the pages.
'''
import searcher
crawler = searcher.crawler('index.db')
crawler.createindextables()
while 1:
    seed_urls = raw_input("Crawling from these urls(divided with ';'):")
    if seed_urls is not None:
        urls = seed_urls.split(';')
        break
crawler.crawl(urls)
