'''This module contains the implementation of the item-based collaborative filtering algorithm.
'''

import math
from operator import itemgetter

# get the item similarity 
def item_similarity(train):
    '''item_similarity(dict) -> dict

    This will return the similarity matrix of the items.
    '''
    sim_matrix = dict() # item similarity matrix
    C = dict() 
    N = dict()

    for u, prefs in train.iteritems():
        for item in prefs.iterkeys():
            N.setdefault(item, 0)
            N[item] += 1
            for other in prefs:
                if item == other:
                    continue
                else:
                    C.setdefault(item, {})
                    C[item].setdefault(other, 0)
                    C[item][other] += 1
    
    for item, co_items in C.iteritems():
        sim_matrix.setdefault(item, {})
        for i, cui in co_items.iteritems():
            sim_matrix[item][i] = cui / math.sqrt(N[item] * N[i] * 1.0)

    return sim_matrix

# get the item similarity with the popularity of the user concernd
def item_similarity_iif(train):
    '''item_similarity_iif(dict) -> dict

    This will improve the coverage percentage of the item-based collaborative filtering by the penalty factor of popular user.
    '''
    sim_matrix = dict()
    C = dict()
    N = dict()

    for u, prefs in train.iteritems():
        for item in prefs.iterkeys():
            N.setdefault(item, 0)
            N[item] += 1
            for other in prefs.iterkeys():
                if item == other:
                    continue
                else:
                    C.setdefault(item, {})
                    C[item].setdefault(other, 0.0)
                    C[item][other] += math.log(1+len(prefs)*1.0)
    item_other = C.items()
    for item, co_items in item_other:
        sim_matrix.setdefault(item, {})
        others = co_items.iteritems()
        for i, cui in others:
            if i not in sim_matrix.iterkeys():
                sim_matrix.setdefault(i, {})
            if item not in sim_matrix[i].iterkeys():

                sim_matrix[i][item] = sim_matrix[item][i] = cui / math.sqrt(N[item] * N[i] * 1.0)

    return sim_matrix


def recommend(user, train, sim_matrix, K=10):
    '''recommend(ini, dict, dict, int) -> dict

    This will return the recommendation based on the item-based collaborative filtering.
    '''
    prefs = train[user]
    rank = dict()

    for item, pi in prefs.iteritems():
        neighbors = sorted(sim_matrix[item].items(), key=itemgetter(1), reverse=True)[0:K]
        for co_item, sim in neighbors:
            if co_item in prefs:
                continue
            else:
                rank.setdefault(co_item, 0.0)
                rank[co_item] += pi * sim
    return rank

        
