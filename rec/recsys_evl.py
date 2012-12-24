'''This module implements some common indexes used to evaluate the effect of recommender algorithm.
'''

import math

# RMSE:root-mean-square error
def rmse(results):
    '''rmse(list) -> float

    Get root-mean-square error from input list of the recommendation results.
    type of results : list.
    results[i] : [uid, iid, rscore, pscore].
    '''

    return math.sqrt(\
            sum([pow(rscore-pscore, 2) for uid, iid,  rscore, prcore in results])\
            / float(len(results)))

# MAE:mean-absolute error
def mae(results):
    '''mae(list) -> float

    Get mean-absolute error from input list of recommendation relults.
    type of results : list.
    results[i] : [uid, iid, rscore, pscore].
    '''

    return sum([abs(rscore-pscore) for uid, iid, rscore, pscore in results])\
            / float(len(results))

# Evaluate the result using precision & recall in (Top-N & 0-1) recommendation 
def get_pecision_recall(n_result, test):
    '''get_precision_recall(dict, dict) -> (float, float)

    Get the precision and recall from input of recommend results compared to the test dataset. The dict contains 'uid : [itemid,...]'.
    '''
    hit = 0
    n_precision = 0
    n_recall = 0
    for user, items in test.items():
        hit  += len(n_result[user] & items)
        n_precision += len(n_result[user])
        n_recall += len(test[user])

    return 'precision: %f, recall: %f' % (hit / (float)n_precision, hit / (float)n_recall)
    
# Evaluate the coverage of the recommend system
def get_coverage(result, items):
    '''get_coverage(dict, list) -> string
    
    This will compute the coverage of the result, and the coverage really tells the ability of discovering the long tail item.
    '''
    result_iid = set() 
    for iid in result.itervalues():
        for i in iid:
            result_iid.add(i)

    return 'coverage: %f' % (len(items) / len(result_iid))

# Get the popularity of the items
def get_popularity(result, items):
    '''get_popularity(dict, list) -> dict

    This is will return the popularity of the items of the result.
    '''
    popularity = dict()
    len_of_result = 0
    for iid in result.itervalues():
        for i in iid:
            popularity.setdefault(i, 0)
            popularity[i] += 1
            len_of_result += 1

    for iid in items:                                       
        if iid not in popularity:                        
            popularity.setdefault(iid, 0)                
        else:                                            
            popularity[iid] /= (float)len_of_result      

    return popularity

