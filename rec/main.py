#!/usr/bin/env python
# filename: main.py
'''The main module of the experiment.
    
'''

import data_processing
    
# Path of the dataset
# path = raw_input('The path of original dataset:')
path = '/home/gxb-hy/dataset/MovieLens/ml-100k/u.data'

M = int(raw_input('Looping M:'))


train, test = data_processing.get_train_test(path, M, 0, 1)

with open('test.data', 'a') as f:
    for k in test:
        f.write(k)
        f.write('\t')
        count = 0
        for v in test[k]:
            count += 1
            f.write(v)
            if count == len(test[k]):
                f.write('\n')
            else:
                f.write('\t')



