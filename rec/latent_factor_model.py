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

