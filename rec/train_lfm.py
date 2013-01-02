#!/usr/bin/env /python
# filename: train_lfm.py
'''This module is used to train the data to get the model.

'''

import data_processing
import latent_factor_model
import cPickle as pickle

# The path of the data source
path = '/home/lishuai/dataset/MovieLens/ml-100k/u.data'

# Get the training set from the data source,
# and the result just has the positive sample
M = int(raw_input('Divide the data to:')) # The original data will be divided to M parts

train, test = data_processing.get_train_test(path, M, 0, 1)

# Get list of all items, the appearance times based on the popularity of item

item_pool = latent_factor_model.get_item_pool(path)

# The sample of all positive and negative for each user
all_sample = dict()

# Get the sample for each user in the training set
for user in train.iterkeys():
    sample = latent_factor_model.random_get_sample(user, item_pool)
    all_sample[user] = sample

# Get the model from the training sample
model_p = dict()
model_q = dict()
model_p, model_q = train_ifm_model(tr_set, 100, 10, 0.02, 0.01)

# Pickle the result for reuse
fp = open('pmatrix', 'w')
fq = open('qmatrix', 'w')
pickle.dump(model_p, fp)
pickle.dump(model_q, fq)

fp.close()
fq.close()

print 'All is done!'

