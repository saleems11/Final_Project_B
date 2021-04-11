from utils.doc_utils import Documents_utils
import Algs.Embedd_DataSet as Emb_D
import Algs.Balancing_Routine as BR
import random as rnd
import numpy as np
import os.path
from Embedded_books.Embed_dataSet import Embed_DataSet


class DataManagement:

    @staticmethod
    def load_data(tweet_size, embedding_size, c1_anchor_size, c2_anchor_size, random_load_c3=False):
        """Load the data for the 5 segments(Cl1, Cl2, Cl3, anchor_Cl1, anchor_Cl2)
        ,the anchor contain data for testing faz that contain(in the first place the anchor and the
        rest are for testing)"""



        """ The code here is better optimized for loading random dataSet for each different time, and better for
        Existing file that doesn't requires embedding them again"""

        embedded_data_c1, embedded_data_c2, embedded_data_c3 = \
            Embed_DataSet.Embed_DataSet(embedding_size=embedding_size, tweet_size=tweet_size)

        embedded_data_c3 = [embedded_data_c3[rnd.randint(0, len(embedded_data_c3) - 1)]]

        embedded_data_c1, embedded_data_c2, embedded_test_c1, embedded_test_c2 = \
            DataManagement.manage_test_data(embedded_data_c1, embedded_data_c2, c1_anchor_size, c2_anchor_size)

        # merge each list of (c1, c2) into one numpy list
        embedded_data_c1 = np.concatenate(embedded_data_c1, axis=0)
        embedded_data_c2 = np.concatenate(embedded_data_c2, axis=0)

        # files_names = ['{0}_{1}.npy'.format(embedding_size, "c1"),
        #                '{0}_{1}.npy'.format(embedding_size, "c2"),
        #                '{0}_{1}.npy'.format(embedding_size, "c3"),
        #                '{0}_{1}.npy'.format(embedding_size, "anchor_c1"),
        #                '{0}_{1}.npy'.format(embedding_size, "anchor_c2")]
        # files_status = [True] * len(files_names)
        #
        # for idx, file_name in enumerate(files_names):
        #     if not os.path.isfile(file_name):
        #         files_status[idx] = False
        #
        # if files_status[0]:
        #     embedded_data_c1 = np.load(files_names[0])
        # else:
        #     c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
        #     c1 = c1[:min(1000, len(c1))]
        # if files_status[1]:
        #     embedded_data_c2 = np.load(files_names[1])
        # else:
        #     c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
        #     c2 = c2[:min(1000, len(c2))]
        # if files_status[2] and not random_load_c3:
        #     # to create new c3 for testing
        #     embedded_data_c3 = np.load(files_names[2], allow_pickle=True)
        # else:
        #     print("New data set for c3 for testing")
        #     c3 = Documents_utils.get_list_of_books(Documents_utils.c3)
        #     c3 = [c3[rnd.randint(0, len(c3) - 1)]]
        # if files_status[3] or files_status[4]:
        #     embedded_test_c1 = np.load(files_names[3], allow_pickle=True)
        #     embedded_test_c2 = np.load(files_names[4], allow_pickle=True)
        # else:
        #     c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
        #     c1 = c1[:min(1000, len(c1))]
        #     c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
        #     c2 = c2[:min(1000, len(c2))]
        #     c1, c2, anchor_c1, anchor_c2 = DataManagement.manage_anchor_data(c1, c2, c1_anchor_size, c2_anchor_size)
        #
        # if not files_status[3] or not files_status[4]:
        #     embedded_test_c1 = []
        #     embedded_test_c2 = []
        # if not files_status[2] or random_load_c3:
        #     embedded_data_c3 = []
        #
        # if embedding_size == 1024:
        #     if not files_status[0]:
        #         embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=tweet_size)
        #     if not files_status[1]:
        #         embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=tweet_size)
        #
        #     if not files_status[2] or random_load_c3:
        #         print("Embedding c3")
        #         for i in range(0, len(c3)):
        #             embedded_data_c3.append(
        #                 Emb_D.Embedd_DataSet.embedd_Elmo(books=np.array([c3[i], ]), tweet_size=tweet_size))
        #
        #     if not files_status[3] or not files_status[4]:
        #         embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=tweet_size)
        #         embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=tweet_size)
        #
        #         for i in range(len(anchor_c1)):
        #             embedded_test_c1.append(
        #                 Emb_D.Embedd_DataSet.embedd_Elmo(books=np.array([anchor_c1[i], ]), tweet_size=tweet_size))
        #
        #         for i in range(len(anchor_c2)):
        #             embedded_test_c2.append(
        #                 Emb_D.Embedd_DataSet.embedd_Elmo(books=np.array([anchor_c2[i], ]), tweet_size=tweet_size))
        #
        # if embedding_size == 300 or embedding_size == 100:
        #     if not files_status[0]:
        #         embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=tweet_size,
        #                                                               embedding_dimension=embedding_size)
        #     if not files_status[1]:
        #         embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=tweet_size,
        #                                                               embedding_dimension=embedding_size)
        #     if not files_status[2] or random_load_c3:
        #         for i in range(0, len(c3)):
        #             embedded_data_c3.append(
        #                 Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([c3[i], ]), tweet_size=tweet_size,
        #                                                    embedding_dimension=embedding_size))
        #
        #     if not files_status[3] or not files_status[4]:
        #         embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=tweet_size,
        #                                                               embedding_dimension=embedding_size)
        #         embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=tweet_size,
        #                                                               embedding_dimension=embedding_size)
        #
        #         for i in range(len(anchor_c1)):
        #             embedded_test_c1.append(
        #                 Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([anchor_c1[i], ]), tweet_size=tweet_size,
        #                                                    embedding_dimension=embedding_size))
        #
        #         for i in range(len(anchor_c2)):
        #             embedded_test_c2.append(
        #                 Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([anchor_c2[i], ]), tweet_size=tweet_size,
        #                                                    embedding_dimension=embedding_size))
        #
        # # save the embedded data
        # if not files_status[0]:
        #     np.save(files_names[0], embedded_data_c1)
        # if not files_status[1]:
        #     np.save(files_names[1], embedded_data_c2)
        # if not files_status[2] or random_load_c3:
        #     np.save(files_names[2], embedded_data_c3, allow_pickle=True)
        # if not files_status[3] or not files_status[4]:
        #     np.save(files_names[0], embedded_data_c1)
        #     np.save(files_names[1], embedded_data_c2)
        #
        #     np.save(files_names[3], embedded_test_c1, allow_pickle=True)
        #     np.save(files_names[4], embedded_test_c2, allow_pickle=True)

        return embedded_data_c1, embedded_data_c2, embedded_data_c3, embedded_test_c1, embedded_test_c2

    @staticmethod
    def manage_test_data(c1, c2, c1_anchor_size, c2_anchor_size):
        # the anchor data set
        test_index_c1 = rnd.sample(range(len(c1)), c1_anchor_size)
        test_index_c2 = rnd.sample(range(len(c2)), c2_anchor_size)
        test_index_c1.sort()
        test_index_c2.sort()

        test_c1 = []
        test_c2 = []

        # remove from c1, c2 the anchor books, and create anchor books list
        for i in range(0, len(test_index_c1)):
            test_c1.append(c1[test_index_c1[i]])

        for i in range(0, len(test_index_c2)):
            test_c2.append(c2[test_index_c2[i]])

        for i in range(0, len(test_index_c1)):
            c1.pop(test_index_c1[i] - i)

        for i in range(0, len(test_index_c2)):
            c2.pop(test_index_c2[i] - i)

        return c1, c2, test_c1, test_c2

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

        # the first value is gazali, the sec is psedo
        y1 = np.tile(np.array([1, 0], dtype='f'), (s1_len, 1))
        y2 = np.tile(np.array([0, 1], dtype='f'), (s2_len, 1))

        # x_train = s1
        # s1 = None
        # x_train = np.concatenate((x_train, s2))

        y_train = y1
        y1 = None
        y_train = np.concatenate((y_train, y2))

        # Random permutation shuffling
        p = np.random.permutation(len(x_train))
        x_train = x_train[p]
        y_train = y_train[p]

        return x_train, y_train
