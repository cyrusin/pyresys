#!/usr/bin/env python
# filename: main_lfm.py
'''The main module of experiment using latent factor model.

'''

import data_processing
import latent_factor_model

# The path of the data source
path = '/home/lishuai/dataset/MovieLens/ml-100k/u.data'

# Looping times, M-fold validation
M = int(raw_input('Looping M:'))

# Get training set and test set from the data source, 
# and the result train just have the positive sample
train, test = data_processing.get_train_test(path, M, 0, 1)

# Get list of all items, the appearance times based on the popularity of item

item_pool = latent_factor_model.get_item_pool(path)

# The sample of all positive and negative for each user
all_sample = dict()

# Get the sample for each user in the training set
for user in train.iterkeys():
    sample = latent_factor_model.random_get_sample(user, item_pool)
    all_sample[user] = sample

