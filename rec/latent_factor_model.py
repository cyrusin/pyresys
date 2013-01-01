'''This module contains the implementation of recommending algorithms based on 
the latent factor model.And the sample function to get the negative sample randomly.
'''

import math
import random

def get_item_pool(path):
    '''get_item_pool(filepath) -> list
    
    This will return a list of items, the item's appearance times is based on 
    the popularity of the item in the original data set.
    '''

    with open(path) as f:

        item_pool = [line.split('\t')[1] for line in f]    

    return item_pool

def random_get_sample(ori_user_prefs, item_pool):
    '''random_get_sample(dict, list) -> dict

    This will return a dict of items with . 
    The algorithm uses the random selection from the item list and the item appearance times
    in this list is based on the popularity.
    '''
    # The sample of items for one user, value (1 or 0) implys the interest of the user to this item
    sample = dict()

    # Get the positive sample
    for item in ori_user_prefs:
        sample[item] = 1              

    # n = 0
    ori_length = len(ori_user_prefs)
    length = len(item_pool)
    
    # Get the negative sample
    for i in xrange(0, ori_length):
        item = item_pool[random.randint(0, length - 1 )]
        if item in sample:
            continue
        else:
            sample[item] = 0

    return sample

def train_ifm_model(tr_set, K, N, learning_rate, penalty):
    '''train_ifm_model(dict, int, int, float, float) -> dict, dict

    This will return the two matrix: user-hiddenClass, hiddenClass-item.
    '''

    # The result matrix P, Q
    P, Q = init_model(tr_set, K)

    # Training process
    for step in range(0, N):
        for user in tr_set.iterkeys():
            for item, rui in tr_set[user].iteritems():
                eui = rui - predict(user, item)
                for k in range(0, K):
                    P[user][k] += learning_rate(eui * Q[item][k] - penalty * P[user][k])
                    Q[item][k] += learning_rate(eui * P[user][k] - penalty * Q[user][k])
        
        learning_rate *= 0.9 # The learning rate should decrease in every iteration step 
        
    return P, Q

def init_model(tr_set, K):
    '''init_model(dict, int) -> dict, dict

    This will return the initiation of the two matrix P, Q.
    The parameter K is the number of the hidden classes. 
    '''
    
    P, Q = dict(), dict()
    # Used to compute the initiation value of the element 
    base = math.sqrt(K)

    for u, i, rui in tr_set.iteritems():
        # Get the initiation of the P: user-hidden(k)
        if u not in P:
            P[u] = [random.random() / base \
                    for x in range(0, K)]

        # Get the initiation of the Q: hidden(k)-item
        if i not in Q:
            Q[i] = [random.random() / base \
                    for x in range(0, K)]

    return P, Q

def predict(user, item, P, Q):
    '''predict(dict, int, dict, dict) -> float

    This will predict the user's rating to the item.
    '''
    rating = 0.0
    length = len(P[user])
    rating = sum(P[user][k] * Q[item][k] for k in xrange(0, length))

    return rating

