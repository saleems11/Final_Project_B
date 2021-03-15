import random as rnd

class Balancing_DataSet:

    @staticmethod
    def Balancing_Routine(d1: [[ [[int]]]], d2: [[ [[int]]]], f1: int, f2: int):
        """ balance the data set according to f1, f2 randomly\n
        !!!!    clould use numpy for better effeciency  !!!!\n
        d1 and d2 are data set containing the representation of each tweet word
        to embedded vectors, f1 is the undersampling rate, f2 is the
        multisampling:parameter\n
        random parts od d1, d2 as s1,s2:returns"""

        if f1<1 or f2<1:
            raise Exception('f1 and f2 should be bigger than 1.'
                            ' The value of f1 was: {0}, The value of f1 was: {1}'.format(
                f1, f2))

        if f1>f2:
            raise Exception('f1 should be smaller than f2.'
                            ' The value of f1 was: {0}, The value of f1 was: {1}'.format(
                f1, f2))

        percent_of_undersampling = 1/f1
        percent_of_multisampling = f1/f2

        size_of_d1 = len(d1)
        size_of_d2 = len(d2)
        d1_rand_indexes = rnd.sample(range(0,size_of_d1),
                                     int(percent_of_undersampling*size_of_d1))
        d2_rand_indexes = rnd.sample(range(0,size_of_d2),
                                     int(percent_of_multisampling*size_of_d2))

        s1=[]
        s2=[]

        for index in d1_rand_indexes:
            s1.append(d1[index])
        for index in d2_rand_indexes:
            s2.append(d2[index])

        return s1, s2