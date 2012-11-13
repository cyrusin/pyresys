import urllib2
import sqlite3 as sqlite
from bs4 import BeautifulSoup
from urlparse import urljoin
ignorewords=set(['the','of','to','and','a','in','is','it'])
class crawler:
	def __init__(self,dbname):
		self.con=sqlite.connect(dbname)
		
	def __del__(self):
		self.con.close()
	def dbcommit(self):
		self.con.commit()
	def getentryid(self,table,field,value,addnew=True):
		return None
	def createindex(self,url,soup):
		if url.isindexed(): return 
		print 'Indexing %s' % url
		
		textfromurl=self.gettext(soup)
		words=self.sprwords(textfromurl)
		urlid=self.getentryid('urltable','url',url)
		for i in range(len(words)):
			word=words[i]
			if word in ignorewords: continue
			wordid=self.getentryid('wordtable','word',word)
			self.con.execute("insert into wordlocationinurl(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))
		
	def gettext(self,soup):
		contentstring=soup.strings
		if contentstring==None:
			spcontents=soup.contents
			result=''
			for content in  spcontents:
				result=result+self.gettext(content)+'\n'
			return result
		else:
			return contentstring.strip()

			
		return None
	//分词
	def sprwords(self,text):
		splitter=re.compile('\\W*')
		return [s.lower() for s in splitter.split(text) if s!='']

	def isindexed(self,url):
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
