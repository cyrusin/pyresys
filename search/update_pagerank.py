#!/usr/bin/env python
# filename: update_pagerank.py
'''This module is running alone to update the pagerank value of each url.'''
import searcher
    
obj = searcher.crawler('index.db')
if obj is not None:
    print 'update pagerank...' 
    obj.getpagerank()
    print 'All pagerank value updated!'
else:
    print 'Failed to update the pagerank value.Make sure the database is OK. '

