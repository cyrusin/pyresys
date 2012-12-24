'''
This module has some useful functions for building a prototype of recommender system.
You can test the algorithm using the data source of MovieLens.If you use other data sets, make sure they are in the correct format.
'''


from math import sqrt

# Get the Euclidean distance of p1 and p2
def get_eucl_distance(prefs, p1, p2):
    '''get_eucl_distance(dict, int, int) -> float

    This will get the disance of p1&p2 based on the Euclidean distance.
    '''
	sim = {}
	for item in prefs[p1]:
		if item in prefs[p2]:
			sim[item] = 1
	if len(sim) == 0:return 0
	sum_of_squares = sum([pow(prefs[p1][item]-prefs[p2][item], 2)
		for item  in prefs[1] if item in prefs[p2]])
	return 1/(1+sqrt(sum_of_squares))

# Get the pearson similarity of p1 and p2
def get_pearson_sim(prefs, p1, p2):
    '''get_pearson_sim(dict, int, int):

    This will get the similarity of p1&p2 based on the Pearson correlation score.
    '''
	sim = {}
	for item in prefs[p1]:
		if item in prefs[p2]: sim[item] = 1
	if len(sim) == 0: return 1
    
    # compute the sum of item score
	sum_p1 = sum([prefs[p1][item] for item in sim])
	sum_p2 = sum([prefs[p2][item] for item in sim])

	sum_sq_p1 = sum([pow(prefs[p1][item], 2) for item in sim])
	sum_sq_p2 = sum([pow(prefs[p2][item], 2) for item in sim])
	pSum = sum([prefs[p1][item] * prefs[p2][item] for item in sim])
	
	num = pSum-(sum_p1 * sum_p2) / n
	den = sqrt((sum1_sq_p1 - pow(sum_p1, 2) / n) * (sum_sq_p2 - pow(sum_p2, 2) / n))

	if den == 0: return 0

	r = num/den

	return r

def getNeighbors(prefs, person, n = 5, similarity = get_pearson_sim):
	scores = [(similarity(prefs, person, other), other) for other in prefs if other!=person]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def getRecommendations(prefs, person, similarity = get_pearson_sim):
	totals = {}
	simSums = {}
	for other in prefs:
		if other == person: continue
		sim = similarity(prefs, person, other)
		if sim <= 0: 
            continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item] * sim
				simSums.setdefault(item, 0)
				simSums[item] += sim
	rankings = [(total / simSums[item], item) for item,total in totals.items()]
	
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

