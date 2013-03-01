#!/usr/bin/env python
# filename: main.py
# Run this module using command "python main.py"
'''This is module is the main method to run the query.'''
import searcher
query_obj = searcher.querying('index.db')
if query_obj is not None:
    while 1:
        query = raw_input('Searching for:')
        if query is not None:
            break
    query_obj.queryrank(query)
else:
    print 'Something wrong with the database!'
