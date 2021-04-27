import gc

import Algs.Balancing_Routine as BR
import numpy as np
from Embedded_books.Embed_dataSet import Embed_DataSet
from Embedded_books.A1 import Embed_data_set
from Objects.TestingData import TestingData


class DataManagement:

    @staticmethod
    def load_data(tweet_size, embedding_size, c1_anchor_name, c2_anchor_name, c1_test_names, c2_test_names, c3_test_names):
        """Load the data for the 5 segments(Cl1, Cl2, Cl3, anchor_Cl1, anchor_Cl2)
        ,the anchor contain data for testing faz that contain(in the first place the anchor and the
        rest are for testing)"""



        """ The code here is better optimized for loading random dataSet for each different time, and better for
        Existing file that doesn't requires embedding them again"""

        # embedded_data_c1, embedded_data_c2, embedded_data_c3, c3_books_names = \
        #     Embed_DataSet.Embed_DataSet(embedding_size=embedding_size, tweet_size=tweet_size)

        # more memory efficient
        embedded_data_c1, embedded_data_c2, embedded_data_c3, c3_books_names = \
            Embed_data_set.embed_data_set(embedding_size=embedding_size, tweet_size=tweet_size)

        testing_data = TestingData(c3=embedded_data_c3, c3_books_names=c3_books_names, c1_anchor_name=c1_anchor_name,
                                   c2_anchor_name=c2_anchor_name, c1_test_names=c1_test_names,
                                   c2_test_names=c2_test_names, c3_test_names=c3_test_names)

        if embedding_size != 1024:
            # merge each list of (c1, c2) into one numpy list
            embedded_data_c1 = np.concatenate(embedded_data_c1, axis=0)
            embedded_data_c2 = np.concatenate(embedded_data_c2, axis=0)

        return embedded_data_c1, embedded_data_c2, testing_data


    @staticmethod
    def create_new_batch(embedded_data_c1, embedded_data_c2):
        # Now lets balance the data
        # s1, s2 = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
        #                                                 embedded_data_c2,
        #                                                 3,
        #                                                 3)

        x_train, s1_len, s2_len = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
                                                         embedded_data_c2,
                                                         3,
                                                         2)

        # the first value is gazali(1, 0), the sec is psedo (0, 1)
        y1 = np.tile(np.array([1, 0], dtype='f'), (s1_len, 1))
        y2 = np.tile(np.array([0, 1], dtype='f'), (s2_len, 1))

        # x_train = s1
        # s1 = None
        # x_train = np.concatenate((x_train, s2))

        y_train = y1
        # del y1
        del embedded_data_c1
        del embedded_data_c2
        y_train = np.concatenate((y_train, y2))
        # del y2
        # free the garbage
        gc.collect()

        # Random permutation shuffling
        # p = np.random.permutation(len(x_train))
        # x_train = x_train[p]
        # y_train = y_train[p]

        return x_train, y_train
