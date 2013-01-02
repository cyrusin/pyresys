#!/usr/bin/env python
# filename: main_lfm.py
'''The main module of experiment using latent factor model.

'''

import data_processing
import latent_factor_model
import cPickle as pickle

# The path of the data source
path = '/home/lishuai/dataset/MovieLens/ml-100k/u.data'

# Looping times, M-fold validation
M = int(raw_input('Looping M:'))

# Get training set and test set from the data source, 
# and the result train just have the positive sample
train, test = data_processing.get_train_test(path, M, 0, 1)



