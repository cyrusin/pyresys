#!/usr/bin/env python
# 
# Using the code does not require permission,unless you incorporate 
# a significant amount of it into your product for commercial profit.
#
# Author: Li Shuai
#
# Time: 2012-12-06

"""The webcrawler and information retrieval tools."""


import urllib2
import re
from urlparse import urljoin
import sqlite3 as sqlite

from bs4 import BeautifulSoup # The third party module.

# Stop-words used to parse the webpage,use a larger set to replace it. 
ignorewords = set(['the','of','to','and','a','in','is','it','this','that','by','so'])

# The web crawler
class crawler:
    # Initiate the crawler class  
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)
    # It is important to close the connection to the database
	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()
    
    # Get the entry id from the table, if not exists, insert it into the table
	def getentryid(self, table, field, value, addnew=True):
		cursor = self.con.execute(\
                "select rowid from %s where %s='%s'" % (table, field, value))
		record = cursor.fetchone()
		if record == None:
			cursor = self.con.execute(\
                    "insert into %s (%s) values ('%s')" % (table, field, value))
			return cursor.lastrowid
		else:
			return record[0]
    
    # Create index for one url using Beautiful soup
	def createindex(self, url, soup):

		if self.isindexed(url): 
            return 
		print 'Indexing '+url
        
        # Get the text content from the web page
		textfromurl = self.gettext(soup)
        # Separate the words from the content
		words = self.sprwords(textfromurl)
        # Get the url id from the data table
		urlid = self.getentryid('urltable', 'url', url)
		for i in range(len(words)):
			word = words[i]
			if word in ignorewords: 
                continue
			wordid = self.getentryid('wordtable', 'word', word)
			self.con.execute(\
                    "insert into wordlocationinurl(urlid, wordid, location) \
                    values (%d, %d, %d)" % (urlid, wordid, i))

	# Get text content 	
	def gettext(self, soup):
		cstring = soup.string
		#print type(cstring)
		if cstring == None:
			spcontents = soup.contents
			result = ''
			for content in  spcontents:
				result=result+self.gettext(content)+'\n'
			return result
		else:
			return cstring.strip()

    # Separate words 
	def sprwords(self,text):
		splitter = re.compile('\\W*')
		return [s.lower() for s in splitter.split(text) if s!='']
 
    # Is the url indexed    
	def isindexed(self, url):
		u = self.con.execute(\
                "select rowid from urltable where url='%s'" % url).fetchone()
		if u != None:
			v = self.con.execute(\
                    'select * from wordlocationinurl \
                    where urlid=%d' % u[0]).fetchone()
			if v != None: return True

		return False

    # Add the link to the linktable
	def addfromtolink(self, urlFrom, urlTo, linkText):
		fromid=self.getentryid('urltable', 'url', urlFrom)
		toid=self.getentryid('urltable', 'url', urlTo)
		self.con.execute('insert into linktable(fromid, toid) \
                        values(%d, %d)' % (fromid, toid))
    # Main method to crawl on the web
	def crawl(self, pages, depth=2):
		for i in range(depth):
			print 'Crawling %d:' % i 
			newpages = set()
			for page in pages:
				try:
					c=urllib2.urlopen(page)
				except:
					print 'Failed to open url:%s' % page
					continue	
				soup = BeautifulSoup(c.read())
				self.createindex(page, soup)
				links = soup.find_all('a')
				for link in links:
					if('href' in dict(link.attrs)):
						url = urljoin(page, link['href'])
						if url.find("'") != -1: 
                            continue
						url = url.split('#')[0]
						if url[0:4] == 'http' and not self.isindexed(url):
							newpages.add(url)
						linkText = self.gettext(link)
						self.addfromtolink(page, url, linkText)
				
				self.dbcommit()
			pages = newpages	
    
    # Create the data index table
	def createindextables(self):
		self.con.execute('create table urltable(url)')
		self.con.execute('create table wordtable(word)')
		self.con.execute('create table wordlocationinurl(urlid,wordid,location)')
		self.con.execute('create table linktable(fromid integer,toid integer)')
		self.con.execute('create table wordforlink(wordid,linkid)')
		self.con.execute('create index wordidx on wordtable(word)')
		self.con.execute('create index urlidx on urltable(url)')
		self.con.execute('create index wordurlidx on wordlocationinurl(wordid)')
		self.con.execute('create index urltoidx on linktable(toid)')
		self.con.execute('create index urlfromidx on linktable(fromid)')
		self.dbcommit()
    # Update the pagerank value 
	def getpagerank(self, iters=10):
		self.con.execute('drop table if exists prtable')
		self.con.execute('create table prtable(urlid primary key,prvalue)')
		self.con.execute('insert into prtable select rowid,1.0 from urltable')
		self.dbcommit()
		
		for i in range(iters):
			print 'Iteration: %d' % (i)
			urls = [row[0] for row in self.con.execute(\
                    'select rowid from urltable')]
			for url in urls:
				pr = 0.15
				urltothis = [row[0] for row in self.con.execute(\
                        'select distinct fromid from linktable \
                        where toid=%d' % url)]
				for link in urltothis:
					outlinknum = self.con.execute(\
                            'select count(*) from linktable \
                            where fromid=%d' % link).fetchone()[0]
					linkpr = self.con.execute(\
                            'select prvalue from prtable \
                            where urlid=%d' % link).fetchone()[0]
					pr += 0.85*(linkpr/outlinknum)
				self.con.execute('update prtable set prvalue=%f \
                        where urlid=%d' % (pr, url))
			self.dbcommit()
	
# The querying class
class querying:

	def __init__(self, dbname):
		self.conn = sqlite.connect(dbname)
		
	def __del__(self):
		self.conn.close()

    # The main method used to do query
	def doquery(self, querystring):

        # Separate the query to single word
		qstring = querystring.strip()
		wordlist = querystring.split(' ')
		wordidlist = []
		lost = []
		fields = 'word0.urlid'
		tables = ''
		clauses = ''
		wordcount = 0
        
        # Get the result for each word of the query string
		for word in wordlist:
			wordrow = self.conn.execute("select rowid from wordtable \
                    where word='%s'" % word).fetchone()
			if wordrow != None:
				wordid = wordrow[0]
				wordidlist.append(wordid)
				if wordcount > 0:
					tables += ','
					clauses += ' and '
					clauses += 'word%d.urlid=word%d.urlid and ' \
                            % (wordcount-1, wordcount)	
				fields += ',word%d.location' % wordcount
				tables += 'wordlocationinurl word%d' % wordcount
				clauses += 'word%d.wordid=%d' % (wordcount, wordid)
				wordcount += 1
			else:
				lost.append(word)

		if len(wordidlist) == 0: 
			print 'No Result!'
			return  

		if len(wordidlist) < len(wordlist):
			print 'Lost some words:'
			print lost

		#print 'select %s from %s where %s' %(fields, tables, clauses)
		queryrows = self.conn.execute('select %s from %s where %s' \
                % (fields, tables, clauses))
		result = [row for row in queryrows]

		resultset = set([row[0] for row in result])
		print 'Result:%d' %(len(resultset))

		return result, wordidlist

	# Get the url name based on the urlid
	def geturlname(self, urlid):
		if urlid != None:
			return self.conn.execute(
				"select url from urltable \
                        where rowid=%d" % urlid).fetchone()[0]
    
    # Get the score of the search results for ranking
	def geturlscoredict(self, queryrows, wordidlist):
		urlscoredict = dict([(row[0], 0) for row in queryrows])
		#weights=[(0.6,self.wordlocation(queryrows)),(0.4,self.worddist(queryrows))]
		#weights=[(1.0,self.countinboundlink(queryrows))]
		#weights=[(1.0,self.wordfrequencyratio(queryrows,wordidlist))]
		weights = [(1.0, self.wordlocation(queryrows)), \
                    (1.0, self.wordfrequency(queryrows)), \
                    (1.0, self.usepagerank(queryrows))]
		for weight, scores in weights:
			for url in urlscoredict:
				urlscoredict[url] += weight*scores[url]
		return urlscoredict	
    
    # Get the search result after ranking
	def queryrank(self,querystring):
		out = self.doquery(querystring)
		if out == None: 
			print 'Failed to search.'
			return
		queryrows, wordidlist = out 
		totalscores = self.geturlscoredict(queryrows, wordidlist)
		rankscores = sorted([(score, urlid) \
                for (urlid, score) in totalscores.items()], reverse=1)
		for (score, urlid) in rankscores[0:20]:
			print '%f\t%s' % (score, self.geturlname(urlid)) 

    # Normalize the scores
	def normalize(self, scores, smallflag=0):
		v = 0.00001
		if smallflag:
			minscore = min(scores.values())
			return dict([(url, float(minscore)/max(v, evl)) \
                    for (url, evl) in scores.items()])
		else:
			maxscore = max(scores.values())
			if maxscore == 0: maxscore = v
			return dict([(url, float(evl)/maxscore) \
                    for (url, evl) in scores.items()])

    # Get the word frequency in each url then normalize it
	def wordfrequency(self, queryrows):
		counts = dict([(row[0], 0) for row in queryrows])
		for row in queryrows:
            counts[row[0]] += 1
		return self.normalize(counts)

    # Get the word frequency ratio compared with the total amount of words 
	def wordfrequencyratio(self, rows, wordidlist):
		total = dict([(row[0], 0) for row in rows])
		wordfreq = []

		for urlid in total.iterkeys():
			total[urlid] = self.conn.execute(\
                    "select count(*) from wordlocationinurl \
                    where urlid=%d" % urlid).fetchone()[0]
			for wordid in wordidlist:
				wordfreq.append(self.conn.execute(\
                        "select count(*) from wordlocationinurl \
                        where wordid=%d and urlid=%d" \
                        % (wordid, urlid)).fetchone()[0])
			temp = min(wordfreq)
			total[urlid] = float(temp) / total[urlid]
		return self.normalize(total)
						
	# Get the location of word in the web page			
	def wordlocation(self, rows):
		wordlocationdict = dict([(row[0], 100000) for row in rows])
		for row in rows:
			locationsum = sum(row[1:])
			if locationsum < wordlocationdict[row[0]]:
                wordlocationdict[row[0]] = locationsum
		return self.normalize(wordlocationdict, smallflag = 1)	

    # Get the distance of the query words in the web page
    # The small distance implies the high score of the url
	def worddist(self, rows):
		if len(rows[0]) <= 2:
            return dict([(row[0], 1.0) for row in rows])
		distances = dict([(row[0], 100000) for row in rows])
        # Find the smallest distance of the words
		for row in rows:
			tempdist = sum([abs(row[i]-row[i-1]) for i in range(2, len(row))])
			if tempdist < distances[row[0]]:
                distances[row[0]] = tempdist
		return self.normalize(distances, smallflag = 1)

    # Get the url score based on the pagerank value
	def usepagerank(self, rows):
		if rows == None:
			print 'Something wrong with usepagerank()!'
			return
		prscore = dict([(row[0], 0) for row in rows])
		for url in prscore:
			prscore[url] = self.conn.execute('select prvalue from prtable \
                    where urlid=%d' % url).fetchone()[0]
		maxvalue = max([prscore[x] for x in prscore])
		for url in prscore:
			prscore[url] = prscore[url] / maxvalue
		return prscore

    # Get the score of the urls based on the amount of inbound links 
	def countinboundlink(self, rows):
		allurls = set([row[0] for row in rows])
		urlnumlist = []
		for url in allurls:
			urlnumlist.append((url, self.conn.execute(
						"select count(*) from linktable where toid=%d" \
                                % url).fetchone()[0]))
		inboundnum = dict(urlnumlist)
		return self.normalize(inboundnum)

    # Get the total amount of the search results
	def totalUrl(self):
		numOfUrl = self.conn.execute('select count(*) from urltable').fetchone()[0]
		print 'total webpages:', numOfUrl
