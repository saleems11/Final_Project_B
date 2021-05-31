import gc
from typing import List

import Algs.Balancing_Routine as BR
import numpy as np
from Embedded_books.A1 import Embed_data_set
from GUI.App.pages.process_bar import ProcessBar
from Objects.TestingData import TestingData


class DataManagement:
    """ A Class  for loading the data and creating new data batch """
    def __init__(self, tweet_size: int, embedding_size: int, c1_anchor_name: List[str], c2_anchor_name: List[str], c1_test_names: List[str],
                 c2_test_names: List[str], c3_test_names: List[str], c1_dir: str, c2_dir: str, c3_dir: str):

        self.tweet_size: int = tweet_size
        self.embedding_size: int = embedding_size
        self.c1_anchor_name: List[str] = c1_anchor_name
        self.c2_anchor_name: List[str] = c2_anchor_name
        self.c1_test_names: List[str] = c1_test_names
        self.c2_test_names: List[str] = c2_test_names
        self.c3_test_names: List[str] = c3_test_names
        self.c1_dir: str = c1_dir
        self.c2_dir: str = c2_dir
        self.c3_dir: str = c3_dir

    def load_data(self, process_bar: ProcessBar):
        """Load the data for the 5 segments(Cl1, Cl2, Cl3, anchor_Cl1, anchor_Cl2)
        ,the anchor contain data for testing phase that contain(in the first place the anchor and the
        rest are for testing), and create TestingData object to save all the prediction result of the model
        :parameters
        process_bar: ProcessBar to update the process bar while loading and embedding the data
        :return
        embedded_data_c1: for training the model over real data
        embedded_data_c2: for training the model over fake data
        testing_data: for testing the model and checking the prediction result
        """

        """ The code here is better optimized for loading random dataSet for each different time, and better for
        Existing file that doesn't requires embedding them again"""

        # embedded_data_c1, embedded_data_c2, embedded_data_c3, c3_books_names = \
        #     Embed_DataSet.Embed_DataSet(embedding_size=embedding_size, tweet_size=tweet_size)

        # more memory efficient
        # the sizes for c1 and c2 for checking if the input of f1, f2 are valid
        embedded_data_c1, embedded_data_c2, embedded_data_c3, c3_books_names, c1_size, c2_size = \
            Embed_data_set.embed_data_set(embedding_size=self.embedding_size, tweet_size=self.tweet_size, c1_dir=self.c1_dir,
                                          c2_dir=self.c2_dir, c3_dir=self.c3_dir, process=process_bar)

        testing_data = TestingData(c3=embedded_data_c3, c3_books_names=c3_books_names, c1_anchor_name=self.c1_anchor_name,
                                   c2_anchor_name=self.c2_anchor_name, c1_test_names=self.c1_test_names,
                                   c2_test_names=self.c2_test_names, c3_test_names=self.c3_test_names)

        if self.embedding_size != 1024:
            # merge each list of (c1, c2) into one numpy list
            embedded_data_c1 = np.concatenate(embedded_data_c1, axis=0)
            embedded_data_c2 = np.concatenate(embedded_data_c2, axis=0)
        process_bar.finished = True
        return embedded_data_c1, embedded_data_c2, testing_data


    @staticmethod
    def create_new_batch(embedded_data_c1, embedded_data_c2, f1=3, f2=2):
        """ create new balanced batch of data for training the model and concatenate them into
        x_train, y_train and shuffle the data
        :parameters
        embedded_data_c1: for training the model over real data
        embedded_data_c2: for training the model over fake data
        f1,f2 multiplying rate
        :returns
        x_train: embedded data set
        y_train: 2d array for indicating the cluster of each tweet
        """
        # Now lets balance the data
        # s1, s2 = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
        #                                                 embedded_data_c2,
        #                                                 3,
        #                                                 3)

        x_train, s1_len, s2_len = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
                                                         embedded_data_c2,
                                                         f1=f1,
                                                         f2=f2)

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
        p = np.random.permutation(len(x_train))
        x_train = x_train[p]
        y_train = y_train[p]

        return x_train, y_train
