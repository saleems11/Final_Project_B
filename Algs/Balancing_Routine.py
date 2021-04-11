import random as rnd
import numpy as np

class Balancing_DataSet:

    @staticmethod
    def Balancing_Routine(d1: [ [[int]]], d2: [ [[int]]], f1: int, f2: int):
        """ balance the data set according to f1, f2 randomly\n
        !!!!    clould use numpy for better effeciency  !!!!\n
        d1 and d2 are data set containing the representation of each tweet word
        to embedded vectors, f1 is the undersampling rate, f2 is the
        multisampling:parameter\n
        random parts of d1, d2 as x_train(s1,s2):returns"""

        if len(d2)>len(d1):
            raise Exception('|d1| must be bigger than |d2|, '
                            '|d1| = {0}, |d2|={1}'.format(len(d1), len(d2)))

        if f1*f2*len(d2)>len(d1):
            raise Exception('f1*f2*|d2|< |d1|'
                            ' The value of f1 was: {0}, The value of f1 was: {1}\n'
                            '|d1| = {2}, |d2|={3}'.format(
                f1, f2, len(d1), len(d2)))

        size_of_d1 = len(d1)
        size_of_d2 = len(d2)
        size_of_s1 = int(size_of_d1/f1)
        d1_rand_indexes = rnd.sample(range(0,size_of_d1), size_of_s1)

        s1 = np.empty(shape=(size_of_s1, len(d1[0]), len(d1[0][0])), dtype='f')
        # s2 = np.repeat(d2, f2, axis=0)

        for i, index in enumerate(d1_rand_indexes):
            s1[i] = d1[index]

        return np.concatenate((s1, np.repeat(d2, f2, axis=0))), len(s1), size_of_d2*f2