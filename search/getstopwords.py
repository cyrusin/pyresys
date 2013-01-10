#!/usr/bin/env python
# filename: getstopwords.py
'''This module is used to get the stop words and pickle it.'''
import pickle
try:
    datafile = open('stop_words_eng.txt')
except IOError , e:
    print e
else:
    stopwords=[]
    
    for line in datafile:
    	word=line.strip()
    	stopwords.append(word)
    
    if len(stopwords) != 0:
        f = open('/home/lishuai/LSGitRepo/PCI_Project/stopwords_pickle', 'w')
        pickle.dump(stopwords, f)
        f.close()
        print 'All is done!'
    else:
        print "There is no stop words."
finally:
    datafile.close()


