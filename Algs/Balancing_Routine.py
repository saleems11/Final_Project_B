import numpy as np
import gc


class Balancing_DataSet:

    @staticmethod
    def Balancing_Routine(d1: [[[int]]], d2: [[[int]]], f1: int, f2: int, reduction_factor=0.8):
        """ balance the data set of (d1, d2) , that is done by repeating d2 data for f1*f2 times
        and saving them in s2, and for d1 |s2|(size of s2) random parts of it is saved into s1.
        :parameter
        d1:[[int]]
        d2:[[int]]
        :returns
        (s1, s2) as a concatenated numpy matrix
        size of s1
        size of s2"""

        if len(d2) > len(d1):
            raise Exception('|d1| must be bigger than |d2|, '
                            '|d1| = {0}, |d2|={1}'.format(len(d1), len(d2)))

        if int(f1 * f2 * len(d2)) > len(d1):
            raise Exception('f1*f2*|d2|< |d1|'
                            ' The value of f1 was: {0}, The value of f1 was: {1}\n'
                            '|d1| = {2}, |d2|={3}'.format(
                f1, f2, len(d1), len(d2)))

        size_of_d1 = len(d1)
        size_of_d2 = len(d2)

        s2 = np.repeat(d2, f2 * f1, axis=0)
        size_of_s2 = len(s2)

        # free d2
        del d2

        d1_rand_indexes = np.random.choice(size_of_d1, size_of_s2, replace=False)
        s1 = d1[d1_rand_indexes]

        # free d1
        del d1

        # free the memory by calling garbage collector
        gc.collect()

        return np.concatenate((s1, s2)), len(s1), len(s2)
