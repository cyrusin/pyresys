import urllib2
import re
import sqlite3 as sqlite
from bs4 import BeautifulSoup
from urlparse import urljoin
#ignorewords=set(['the','of','to','and','a','in','is','it','this','that','by','so'])
class crawler:
	def __init__(self,dbname):
		self.con=sqlite.connect(dbname)
		
	def __del__(self):
		self.con.close()
	def dbcommit(self):
		self.con.commit()
	def getentryid(self,table,field,value,addnew=True):
		cursor=self.con.execute("select rowid from %s where %s='%s'" % (table,field,value))
		record=cursor.fetchone()
		if record==None:
			cursor=self.con.execute("insert into %s (%s) values ('%s')" % (table,field,value))
			return cursor.lastrowid
		else:
			return record[0]
	def createindex(self,url,soup):
		if self.isindexed(url): return 
		print 'Indexing '+url
		
		textfromurl=self.gettext(soup)
		words=self.sprwords(textfromurl)
		urlid=self.getentryid('urltable','url',url)
		for i in range(len(words)):
			word=words[i]
			if word in ignorewords: continue
			wordid=self.getentryid('wordtable','word',word)
			self.con.execute("insert into wordlocationinurl(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))
		
	def gettext(self,soup):
		cstring=soup.string
		print type(cstring)
		if cstring==None:
			spcontents=soup.contents
			result=''
			for content in  spcontents:
				result=result+self.gettext(content)+'\n'
			return result
		else:
			return cstring.strip()

	def sprwords(self,text):
		splitter=re.compile('\\W*')
		return [s.lower() for s in splitter.split(text) if s!='']

	def isindexed(self,url):
		u=self.con.execute("select rowid from urltable where url='%s'" % url).fetchone()
		if u!=None:
			v=self.con.execute('select * from wordlocationinurl where urlid=%d' % u[0]).fetchone()
			if v!=None: return True
		return False
	def addfromtolink(self,urlFrom,urlTo,linkText):
		pass
	def crawl(self,pages,depth=2):
		for i in range(depth):
			print 'Crawling %d:' % i 
			newpages=set()
			for page in pages:
				try:
					c=urllib2.urlopen(page)
				except:
					print 'Failed to open url:%s' % page
					continue	
				soup=BeautifulSoup(c.read())
				self.createindex(page,soup)
				links=soup.find_all('a')
				for link in links:
					if('href' in dict(link.attrs)):
						url=urljoin(page,link['href'])
						if url.find("'")!=-1: continue
						url=url.split('#')[0]
						if url[0:4]=='http' and not self.isindexed(url):
							newpages.add(url)
						linkText=self.gettext(link)
						self.addfromtolink(page,url,linkText)
				
				self.dbcommit()
			pages=newpages	
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

class querying:
	def __init__(self,dbname):
		self.conn=sqlite.connect(dbname)
		
	def __del__(self):
		self.conn.close()

	def doquery(self,querystring):
		qstring=querystring.strip()
		wordlist=qstring.split(' ')
		wordidlist=[]
		fields='word0.urlid'
		tables=''
		clauses=''
		
		wordcount=0
		for word in wordlist:
			wordrow=self.conn.execute(
				"select rowid from wordtable where word='%s'" % word).fetchone()
			if wordrow!=None:
				wordid=wordrow[0]
				wordidlist.append(wordid)
				if wordcount>0:
					tables+=','
					clauses+=' and '
					clauses+='word%d.urlid=word%d.urlid and ' % (wordcount-1,wordcount)	
				fields+=',word%d.location' % wordcount
				tables+='wordlocationinurl word%d' % wordcount
				clauses+='word%d.wordid=%d' % (wordcount,wordid)
				wordcount+=1
		queryrow=self.conn.execute('select %s from %s where %s' % (fields,tables,clauses))
		result=[row for row in queryrow]
		return result,wordidlist
	
	def geturlname(self,urlid):
		if urlid != None:
			return self.conn.execute(
				"select url from urltable where rowid=%d" % urlid).fetchone()[0]

	def geturlscoredict(self,queryrows,wordidlist):
		urlscoredict=dict([(row[0],0) for row in queryrows])
		weights=[(1.0,self.wordlocation(queryrows))]
		for (weight,scores) in weights:
			for url in urlscoredict:
				urlscoredict[url]+=weight*scores[url]
		return urlscoredict	
	def queryrank(self,querystring):
		queryrows,wordidlist=self.doquery(querystring)
		totalscores=self.geturlscoredict(queryrows,wordidlist)
		rankscores=sorted([(score,urlid) for (urlid,score) in totalscores.items()],reverse=1)
		for (score,urlid) in rankscores[0:10]:
			print '%f\t%s' % (score,self.geturlname(urlid)) 

	def normalize(self,scores,smallflag=0):
		v=0.00001
		if smallflag:
			minscore=min(scores.values())
			return dict([(url,float(minscore)/max(v,evl)) for (url,evl) in scores.items()])
		else:
			maxscore=max(scores.values())
			if maxscore==0: maxscore=v
			return dict([(url,float(evl)/maxscore) for (url,evl) in scores.items()])

	def wordfrequency(self,rows):
		counts=dict([(row[0],0) for row in rows])
		for row in rows: counts[row[0]]+=1
		return self.normalize(counts)

	def wordlocation(self,rows):
		wordlocationdict=dict([(row[0],100000) for row in rows])
		for row in rows:
			locationsum=sum(row[1:])
			if locationsum<wordlocationdict[row[0]]: wordlocationdict[row[0]]=locationsum
		return self.normalize(wordlocationdict,smallflag=1)	
