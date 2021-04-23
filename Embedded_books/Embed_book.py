import numpy as np
import os.path

from Algs.Embedd_DataSet import Embedd_DataSet
from utils.doc_utils import Documents_utils


class Embed_book:

    @staticmethod
    def embed_book_and_save_1024(cluster_name, file_name, embedding_size, tweet_size, cluster_dir):

        curr_book_path = os.path.join(cluster_dir, file_name)

        if embedding_size == 1024:
            # embed using Elmo

            # embedded_file_name = '{0}_{1}_{2}.npy'.format(file_name[:-4], embedding_size, tweet_size)
            embedded_file_name = Embed_book.convert_file_name_to_embedded_name(file_name=file_name,
                                                                               embedding_size=embedding_size,
                                                                               tweet_size=tweet_size)
            embedded_file_name = embedded_file_name[0]

            books_cluster_dir = Embed_book.get_book_cluster_dir_path(cluster_name=cluster_name)

            book_embedding_path = books_cluster_dir + "\\" + embedded_file_name
            # check if file exist
            if os.path.isfile(book_embedding_path):
                return

            # there is No prev embedded book
            # load the text file
            embedded_data = Embedd_DataSet.embedd_Elmo(books=[Documents_utils.read_doc_file(curr_book_path)],
                                                       tweet_size=tweet_size)

            # save the file
            # check if dir exist
            if not os.path.isdir(books_cluster_dir):
                os.mkdir(books_cluster_dir)

            np.save(book_embedding_path, embedded_data)
            return

        raise Exception("invalid embedding_size"+str(embedding_size))

    @staticmethod
    def embed_book_AraVec(file_name, embedding_size, tweet_size, cluster_dir):
        curr_book_path = os.path.join(cluster_dir, file_name)

        if embedding_size == 300 or embedding_size == 100:
            # embed using AraVec
            return Embedd_DataSet.embedd_Aravec(books=[Documents_utils.read_doc_file(curr_book_path)],
                                                tweet_size=tweet_size,
                                                embedding_dimension=embedding_size)

        raise Exception("invalid embedding_size" + str(embedding_size))


    @staticmethod
    def load_npy_file_appen_to_main_matrix(file_path, main_array, start_idx, lenght):
        """ merge a numpy array to the main array and return the updated idx"""
        main_array[start_idx: start_idx+lenght] = np.load(file_path)
        return start_idx+lenght


    @staticmethod
    def convert_file_name_to_embedded_name(files_names: [str], embedding_size: int, tweet_size: int) -> [str]:
        """ Convert name of a File to name of file that appropriate for the embedded books data"""
        embedded_names = []
        for file_name in files_names:
            embedded_names.append('{0}_{1}_{2}.npy'.format(file_name[:-4], embedding_size, tweet_size))

        return embedded_names

    @staticmethod
    def get_book_cluster_dir_path(cluster_name):
        return "\\".join([Documents_utils.project_working_dir, "Embedded_books", cluster_name])
