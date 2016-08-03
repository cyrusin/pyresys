#pyresys

This project includes implemetation of some intelligent algorithms:

1. Recommender system
2. Lightweight search engine
3. Data clustering

Main Content
----------------
	Web crawling
	Indexing the web page
	Searching
	Build a recommender system
	Data clustering

Detail of all the algorithms
--------
Top-N Recommender System:

    Collaborative Filtering : User-based
    Collaborative Filtering : Item-based
    Latent Factor Model: SVD(singular value decomposition)
	Evaluation of the performance: Recall, Precision, Coverage, Popularity 
    Dataset for test : MovieLens
		
Lightweight search engine:

	Use BeautifulSoup and urllib2 to parse the .html
	Get the score of the web page for ranking based on the content,pagerank
	Use SQLite as database

Data clustering:

    Hierarchical clustering
    K-means clustering

How to use the  lightweight search engine
-----------------------------------
- All the main methods are in the module of `search/searcher.py`
- Crawl: `python search/crawl.py`
- Update the pagerank value: `python search/update_pagerank.py`
- Search: `python search/main.py`


