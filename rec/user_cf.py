'''This module contains the collaborative filtering algorithms based on user similarity.

'''

import math
from operator import itemgetter

def user_sim_matrix(train):
    '''user_sim_matrix(dict) -> dict

    This will return the user similarity matrix. Use it when the train set is not very large.
    '''
    sim_matrix = dict()
    for p1 in train.iterkeys():
        for p2 in train.iterkeys():
            if p1 == p2:
                continue
            else:
                result = len(train[p1] & train[p2])
                sim_matrix[p1][p2] = result / math.sqrt((len(train[p1]) * len(train[p2]) * 1.0))

    return sim_matrix

def user_similarity(train):
    '''user_similarity(dict) -> dict

    This will return the user similarity matrix. 
    It uses the item-users inverse table to make the computing process fast.
    '''
    sim_matrix = dict()
    item_users = dict()
    
    # build the item-users inverse table
    for user, prefs in train.iteritems():
        for item in prefs.iterkeys():
            if item not in item_users:
                item_users[item] = set()
            item_users[item].add(user)
    # compute the co-rated items between the users
    C = dict() 
    N = dict() 
    for item, users in item_users.iteritems():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                else:
                    C.setdefault(u, {})
                    C[u].setdefault(v, 0)
                    C[u][v] += 1

    # get the sim_matrix
    for user, co_users in C.iteritems():
        sim_matrix.setdefault(user, {})
        for v, cuv in co_users.iteritems():
            sim_matrix.setdefault(v, {})
            #sim_matrix[user].setdefault(v, 0.0)
            if user not in sim_matrix[v]:
                sim_matrix[v][user] = sim_matrix[user][v] = cuv / math.sqrt(N[user] * N[v] * 1.0)

    return sim_matrix

# another implementation of the user similarity based on the popularity of the item
def user_similarity_iif(train):
    '''user_similarity_iif(dict) -> dict

    This function will return the user similarity matrix based on the popularity of the item
    which is preferd by one user and another.
    It first uses the inverse table of the item-users to make the computing process fast.
    '''
    sim_matrix = dict()
    item_users = dict()
    # build the item-users inverse table
    for user, prefs in train.iteritems():
        for item in prefs.iterkeys():
            if item not in item_users:
                item_users[item] = set()
            item_users[item].add(user)
    
    C = dict() # this matrix contains the intersection of every two users
    N = dict() # this matrix contains the num of items each user' preference

    for item, users in item_users.iteritems():
        # The popularity of the item
        pop = 1 / math.log(1+len(users))
        for u in users:
            C.setdefault(u, {})
            N.setdefault(u, 0)
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                else:
                    C[u].setdefault(v, 0.0)
                    C[u][v] += pop

    for user, co_users in C.iteritems():
        sim_matrix.setdefault(user, {})
        for v, cuv in co_users.iteritems():
            sim_matrix.setdefault(v, {})
            if user not in sim_matrix[v]:
                sim_matrix[v][user] = sim_matrix[user][v] = cuv / math.sqrt((N[user] * N[v]*1.0))

    return sim_matrix
            
# recommend to user
def recommend(user, train, sim_matrix, K=30):
    '''recommend(int, dict, dict, int) -> dict

    This will return the recommendation to the user based the user's k neighbors.
    '''
    rank = dict()
    user_prefs = train[user]

    neighbors = sorted(sim_matrix[user].iteritems(), key = itemgetter(1), reverse = True)[0:K]
    for v, sim_uv in neighbors:
        for item, score in train[v].iteritems():
            if item in user_prefs:
                continue
            else:
                rank.setdefault(item, 0.0)
                rank[item] += sim_uv * score

    return rank


