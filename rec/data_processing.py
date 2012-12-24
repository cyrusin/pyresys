'''This is module contains the methods of processing the data.

The data may comes from MovieLens or other.
'''

import random

def get_train_test(path, M, k, seed):
    '''get_train_test(str, int, int, int) -> dict, dict

    This will generate the trainset and testset based on the original dataset. 
    0 <= k <= M-1.So call this function for M times and do the experiment each time.
    '''
    test = {}
    train = {}
    random.seed(seed)

    with open(path) as f:
        for line in f:
            user, item = line.split('\t')[0:2]
            if random.randint(0, M) == k:
                test.setdefault(user, [])
                test[user].append(item)
            else:
                train.setdefault(user, [])
                train[user].append(item)

    return train, test


