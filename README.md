pyresys
=======

This project includes frameworks of some intelligent applications:recommender system,information retrieval,data clustering,etc.

#Targets
	Webcrawler
	Indexing
	Searching
	Recommender
	Dataclustering
#Details
	RecommenderSystem
		1)user-based
		2)item-based
		3)dataset:movielens
		4)similaritymeasure:Euclidean distance,Pearson correlation
	InformationRetrieval
		1)use BeautifulSoup and urllib2 to parse the .html
		2)compute the score of the webpage based on the content
		3)use  SQLite as database  
	DataClustering
		1)hierarchical clustering
		2)K-means clustering
#Uses
	crawling:
		>>>import searcher
		>>>e=searcher.crawler('xxx.db')#the db you want to use for storing the data
		>>>e.createindextables()
		>>>pages=['http://...','http://...',...]#urllist
		>>>e.crawl(pages)
	searching:
		>>>import searcher
		>>>e=searcher.querying('xxx.db')
		>>>e.queryrank('python programming')#fill in the query words
