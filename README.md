#pyresys

This project includes frameworks of some intelligent applications:
(1)recommender system,(2)lightweight search engine,(3)data clustering.

What can it do?
----------------
	web crawling
	create index for the web page
	search
	build a recommender system
	data clustering
Details
--------
	-Top-N Recommender System:
		1)Collaborative Filtering : User-based
		2)Collaborative Filtering : Item-based
		3)Latent Factor Model: SVD(singular value decomposition)
		4)Evaluation of the performance: Recall, Precision, Coverage, Popularity 
		5)Dataset for test : MovieLens
		
	-Lightweight search engine:
		1)Use BeautifulSoup and urllib2 to parse the .html
		2)Get the score of the web page for ranking based on the content,pagerank
		3)Use  SQLite as database  
	-Data clustering
		1)Hierarchical clustering
		2)K-means clustering
About the lightweight search engine
-----------------------------------
- All the main methods are in the module of 'search/searcher.py'.
- The other module: 'search/crawl.py', 'search/update_pagerank.py', 'search/main.py' will run alone to do what you want: crawling, update the page rank value, and response to the query.
-Crawl: 'python search/crawl.py'.
-Update the pagerank value: 'python search/update_pagerank.py'.
-Search: 'python search/main.py'


