#!/usr/bin/env python
# filename: main_lfm.py
'''The main module of experiment using latent factor model.
This is mainly used to get the recommendation for all users.

'''

import latent_factor_model
import cPickle as pickle

# Load P, Q, trainingset, testset
path = '/home/lishuai/work/lfm/test6/'

fp = open(path+'pmatrix', 'r')
P = pickle.load(fp)
fp.close()

fq = open(path+'qmatrix', 'r')
Q = pickle.load(fq)
fq.close()

ftr = open(path+'trainset')
train = pickle.load(ftr)
ftr.close()

fte = open(path+'testset')
test = pickle.load(fte)
fte.close()

# Get recommedation to all users
result = dict()
for u in train.iterkeys():
    prefs = latent_factor_model.recommend(u, train, P, Q)
    result[u] = prefs

# Pickle the result
f = open(path+'recommendation', 'w')
pickle.dump(result, f)
f.close()

print 'All is done!'

