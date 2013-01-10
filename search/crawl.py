#!/usr/bin/env python
# filename: crawl.py
'''This module is used to crawing the web pages and 
build index for all the pages.
'''

import searcher

crawler = searcher.crawler('index.db')
crawler.createindextables()
urls = ['http://kiwitobes.com/wiki/Categorical_list_of_programming_languages.html']
crawler.crawl(urls)

