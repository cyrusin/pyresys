'''This module implements some common indexes used to evaluate the effect of recommender algorithm.
'''

import math

# root-mean-square error
def rmse(results):
    '''rmse(list) -> float

    Get root-mean-square error from input list of the recommendation results.
    type of results : list.
    results[i] : [uid, iid, rscore, pscore].
    '''

    return math.sqrt(
            sum([pow(rscore-pscore, 2) for uid, iid,  rscore, prcore in results])
            / float(len(results)))



