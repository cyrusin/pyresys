'''This module contains the implementation of the item-based collaborative filtering algorithm.
'''

import math
from operator import itemgetter

def item_similarity(train):
    '''item_similarity(dict) -> dict

    This will return the similarity matrix of the items.
    '''
    sim_matrix = dict() # item similarity matrix
    C = dict() 
    N = dict()

    for u, prefs in train.items():
        for item in prefs.keys():
            N[item] += 1
            for other in prefs.keys():
                if item == other:
                    continue
                else:
                    C.setdefault(item, {})
                    C[item].setdefault(other, 0)
                    C[item][other] += 1
    
    for item, co_items in C.items():
        sim_matrix.setdefault(item, {})
        for i, cui in co_items.items():
            sim_matrix[item][i] = cui / math.sqrt(N[item] * N[i] * 1.0)

    return sim_matrix

def recommend(user, train, sim_matrix, K=10):
    '''recommend(ini, dict, dict, int) -> dict

    This will return the recommendation based on the item-based collaborative filtering.
    '''
    prefs = train[user]
    rank = dict()

    for item, pi in prefs.items():
        neighbors = sorted(sim_matrix[item].items(), key=itemgetter(1), reverse=True)[0:k]
        for co_item, sim in neighbors:
            if co_item in prefs:
                continue
            else:
                rank.setdefault(co_item, 0.0)
                rank[co_item] += pi * sim
    return rank

        
