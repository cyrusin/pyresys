#!/usr/bin/env python
# filename: main.py
'''The main module of the experiment.
    
'''

import data_processing
import user_cf
#import item_cf
import recsys_evl
    
# Path of the dataset
# path = raw_input('The path of original dataset:')
#path = '/home/gxb-hy/dataset/MovieLens/ml-100k/u.data'
path = '/home/lishuai/dataset/MovieLens/ml-100k/u.data'

# loopting times, M-fold cross validation
M = int(raw_input('Looping M:')) 

train, test = data_processing.get_train_test(path, M, 0, 1)

# test.data is used to store the temp test data
# with open('test.data', 'a') as f:
#     for k in test:
#         f.write(k)
#         f.write('\t')
#         count = 0
#         for v in test[k]:
#             count += 1
#             f.write(v)
#             if count == len(test[k]):
#                 f.write('\n')
#             else:
#                 f.write('\t')

# get the user similarity matrix from the user similarity based on penalty of the item popularity 
sim_matrix = user_cf.user_similarity_iif(train)

# get the user similarity matrix from the common user similarity 
#sim_matrix = user_cf.user_similarity(train)

# get the item similarity matrix from the item similarity based on penalty of the user popularity
#sim_matrix = item_cf.item_similarity_iif(train)

# get the recall 
recall = recsys_evl.get_recall(train, test, user_cf.recommend, sim_matrix)
#get the precision
precision = recsys_evl.get_precision(train, test, user_cf.recommend, sim_matrix)

print recall, precision

