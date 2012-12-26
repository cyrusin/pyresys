'''This module contains the collaborative filtering algorithms based on user similarity.

'''

import math


def user_sim_matrix(train):
    '''user_sim_matrix(dict) -> dict

    This will return the user similarity matrix. Use it when the train set is not very large.
    '''
    sim_matrix = dict()
    for p1 in train.keys():
        for p2 in train.keys():
            if p1 == p2:
                continue
            else:
                result = len(train[p1] & train[p2])
                sim_matrix[p1][p2] = result / math.sqrt((len(train[p1]) * len(train[p2]) * 1.0))

    return sim_matrix

def user_similarity(train):
    '''user_similarity(dict) -> dict

    This will return the user similarity matrix. 
    It uses the item-users inverse table to make the computing process easy.
    '''
    sim_matrix = dict()
    item_users = dict()
    
    # build the item-users inverse table
    for user, prefs in train.items():
        for item in prefs.keys():
            if item not in item_users:
                item_users[item] = set()
         item_user[item].add(user)
    # compute the co-rated items between the users
    C = dict() 
    N = dict() 
    for item, users in item_user.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                else:
                    C[u][v] += 1

    # get the sim_matrix
    for user, co_users in C.items():
        for v, cuv in co_users.items():
            sim_matrix[user][v] = cuv / math.sqrt(N(user) * N(v))

    return sim_matrix

