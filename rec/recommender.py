'''
This module has some useful functions for building a prototype of recommender system.
You can test the algorithm using the data source of MovieLens.If you use other data sets, make sure they are in the correct format.
'''


from math import sqrt


def sim_distance(prefs, person1, person2):
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item] = 1
	if len(si) == 0:return 0
	sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2)
		for item  in prefs[person1] if item in prefs[person2]])
	return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, p1, p2):
	si = {}
	for item in prefs[p1]:
		if item in prefs[p2]: si[item] = 1
	n = len(si)
	if n == 0: return 1
	sum1 = sum([prefs[p1][it] for it in si])
	sum2 = sum([prefs[p2][it] for it in si])

	sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
	sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
	pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])
	
	num = pSum-(sum1*sum2/n)
	den = sqrt((sum1Sq-pow(sum1, 2)/n)*(sum2Sq-pow(sum2, 2)/n))
	if den == 0: return 0

	r = num/den

	return r

def topMatches(prefs, person, n = 5, similarity = sim_pearson):
	scores = [(similarity(prefs, person, other), other) for other in prefs if other!=person]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def getRecommendations(prefs, person, similarity = sim_pearson):
	totals = {}
	simSums = {}
	for other in prefs:
		if other == person: continue
		sim = similarity(prefs, person, other)
		if sim<=0: continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item]*sim
				simSums.setdefault(item, 0)
				simSums[item] += sim
	rankings = [(total/simSums[item], item) for item,total in totals.items()]
	
	rankings.sort()
	rankings.reverse()
	return rankings

def traneformPrefs(prefs):
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person] = prefs[person][item]
	return result

def calculateSimilarItems(prefs,n=10):
	result = {}
	itemPrefs=transformPrefs(prefs)
	c = 0
	for item in itemPrefs:
		c += 1
		if c%100==0: print "%d / %d" % (c, len(itemPrefs))
		scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
		result[item] = scores
	return result

def getRecommendedItems(prefs, itemMatch, user):
	userRatings = prefs[user]
	scores = {}
	totalSim = {}
	for(item, rating) in userRatings.items():
		for (similarity, item2) in itemMatch[item]:
			if item2 in userRatings: continue
			scores.setdefault(item2, 0)
			scores[item2] += similarity*rating
			totalSim.setdefault(item2, 0)
			totalSim[item2] += similarity
	rankings=[(score/totalSim[item], item) for item,score in scores.items()]
	rankings.sort()
	rankings.reverse()
	return rankings

def loadMovieLens(path):
	movies = ()
	for line in open(path):
		(id,title) = line.split('|')[0:2]
		movie[id] = title
	prefs = {}
	for line in open(path):
		(user,movieid,rating,ts) = line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]] = float(rating)
	return prefs

def loadMovielens(path='/home/asus/dataset'):
	movies = {}
	for line in open(path+"/ml-100k/u.item"):
		(id,title) = line.split("|")[0:2]
		movies[id] = title
		
	prefs = {}
	for line in open(path+"/ml-100k/u.data"):
		(uid,iid,ratings,time) = line.split('\t')
		prefs.setdefault(uid,{})
		prefs[uid][movies[iid]] = float(ratings)
	return prefs

