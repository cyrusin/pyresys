#!/usr/bin/env python
# filename: lfm_evl.py
'''This module is used to evaluate the precision and recall of the lfm model.

'''

import latent_factor_model
import cPickle as pickle

# Load test, result
path = '/home/lishuai/work/lfm/test4/'

fte = open(path+'testset', 'r')
test = pickle.load(fte)
fte.close()

fre = open(path+'recommendation', 'r')
result = pickle.load(fre)
fre.close()

# Get the precision and recall
print latent_factor_model.get_precision(result, test)
print latent_factor_model.get_recall(result, test)
