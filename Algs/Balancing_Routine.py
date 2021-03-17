import random as rnd
import numpy as np

class Balancing_DataSet:

    @staticmethod
    def Balancing_Routine(d1: [[ [[int]]]], d2: [[ [[int]]]], f1: int, f2: int):
        """ balance the data set according to f1, f2 randomly\n
        !!!!    clould use numpy for better effeciency  !!!!\n
        d1 and d2 are data set containing the representation of each tweet word
        to embedded vectors, f1 is the undersampling rate, f2 is the
        multisampling:parameter\n
        random parts od d1, d2 as s1,s2:returns"""

        if f1*f2*len(d2)>len(d1):
            raise Exception('f1*f2*|d2|< |d1|'
                            ' The value of f1 was: {0}, The value of f1 was: {1}\n'
                            '|d1| = {2}, |d2|={3}'.format(
                f1, f2, len(d1), len(d2)))

        size_of_d1 = len(d1)
        size_of_d2 = len(d2)
        d1_rand_indexes = rnd.sample(range(0,size_of_d1), size_of_d2)

        s1 = np.empty(shape=(size_of_d2*f1, len(d1[0]), len(d1[0][0])))
        s2 = np.repeat(d2, f2, axis=1)

        i=0
        for index in d1_rand_indexes:
            # copy the same data for f1 times
            for j in range(0,f1):
                s1[i+j*size_of_d2] = d1[index]
            i += 1



        return s1, s2