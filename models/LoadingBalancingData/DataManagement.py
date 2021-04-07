from utils.doc_utils import Documents_utils
import Algs.Embedd_DataSet as Emb_D
import Algs.Balancing_Routine as BR
import random as rnd
import numpy as np

class DataManagement:

    @staticmethod
    def load_data(tweet_size, embedding_size, c1_anchor_size, c2_anchor_size):
        """Load the data for the 5 segments(Cl1, Cl2, Cl3, anchor_Cl1, anchor_Cl2)
        ,the anchor contain data for testing faz that contain(in the first place the anchor and the
        rest are for testing)"""

        c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
        c1 = c1[:min(1000, len(c1))]
        c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
        c2 = c2[:min(1000, len(c2))]
        c3 = Documents_utils.get_list_of_books(Documents_utils.c3)
        c3 = [c3[rnd.randint(0, len(c3)-1)]]

        c1, c2, anchor_c1, anchor_c2 = DataManagement.manage_anchor_data(c1, c2, c1_anchor_size, c2_anchor_size)

        embedded_anchor_c1 = []
        embedded_anchor_c2 = []
        embedded_data_c3 = []

        if embedding_size == 1024:
            embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=tweet_size)
            embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=tweet_size)

            for i in range(0, len(c3)):
                embedded_data_c3.append(
                    Emb_D.Embedd_DataSet.embedd_Elmo(books=np.array([c3[i], ]), tweet_size=tweet_size))

            for i in range(len(anchor_c1)):
                embedded_anchor_c1.append(
                    Emb_D.Embedd_DataSet.embedd_Elmo(books=np.array([anchor_c1[i], ]), tweet_size=tweet_size))

            for i in range(len(anchor_c2)):
                embedded_anchor_c2.append(
                    Emb_D.Embedd_DataSet.embedd_Elmo(books=np.array([anchor_c2[i], ]), tweet_size=tweet_size))

        if embedding_size == 300 or embedding_size == 100:
            embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=tweet_size,
                                                                  embedding_dimension=embedding_size)
            embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=tweet_size,
                                                                  embedding_dimension=embedding_size)

            for i in range(0, len(c3)):
                embedded_data_c3.append(
                    Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([c3[i], ]), tweet_size=tweet_size,
                                                       embedding_dimension=embedding_size))

            for i in range(len(anchor_c1)):
                embedded_anchor_c1.append(
                    Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([anchor_c1[i], ]), tweet_size=tweet_size,
                                                       embedding_dimension=embedding_size))

            for i in range(len(anchor_c2)):
                embedded_anchor_c2.append(
                    Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([anchor_c2[i], ]), tweet_size=tweet_size,
                                                       embedding_dimension=embedding_size))

        return embedded_data_c1, embedded_data_c2, embedded_data_c3, embedded_anchor_c1, embedded_anchor_c2



    @staticmethod
    def manage_anchor_data(c1, c2, c1_anchor_size, c2_anchor_size):
        # the anchor data set
        anchor_index_c1 = rnd.sample(range(len(c1)), c1_anchor_size)
        anchor_index_c2 = rnd.sample(range(len(c2)), c2_anchor_size)
        anchor_index_c1.sort()
        anchor_index_c2.sort()

        anchor_c1 = []
        anchor_c2 = []

        # remove from c1, c2 the anchor books, and create anchor books list
        for i in range(0, len(anchor_index_c1)):
            anchor_c1.append(c1[anchor_index_c1[i]])

        for i in range(0, len(anchor_index_c2)):
            anchor_c2.append(c2[anchor_index_c2[i]])

        for i in range(0, len(anchor_index_c1)):
            c1.pop(anchor_index_c1[i] - i)

        for i in range(0, len(anchor_index_c2)):
            c2.pop(anchor_index_c2[i] - i)

        return c1, c2, anchor_c1, anchor_c2


    @staticmethod
    def create_new_batch(embedded_data_c1, embedded_data_c2):
        # Now lets balance the data
        s1, s2 = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
                                                        embedded_data_c2,
                                                        3,
                                                        2)

        # the first value is gazali, the sec is psedo
        y1 = np.tile(np.array([1, 0], dtype='f'), (len(s1), 1))
        y2 = np.tile(np.array([0, 1], dtype='f'), (len(s2), 1))

        x_train = s1
        s1 = None
        x_train = np.concatenate((x_train, s2))

        y_train = y1
        y1 = None
        y_train = np.concatenate((y_train, y2))

        # Random permutation shuffling
        p = np.random.permutation(len(x_train))
        x_train = x_train[p]
        y_train = y_train[p]

        return x_train, y_train