import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
ignorewords=set(['the','of','to','and','a','in','is','it'])
class crawler:
	def __init__(self,dbname):
		pass
	def __del__(self):
		pass

	def dbcommit(self):
		pass
	def getentryid(self,table,field,value,addnew=True):
		return None
	def createindex(self,url,soup):
		print 'Indexing %s' % url
	def gettext(self,soup):
		return None
	def sprwords(self,text):
		return None

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
		pass



