import os

from utils.doc_utils import Documents_utils
from Embedded_books.Embed_book import Embed_book
import numpy as np


class Embed_DataSet:

    @staticmethod
    def Embed_DataSet(embedding_size, tweet_size):
        c1_books_names = Documents_utils.get_list_of_docs_files(Documents_utils.c1)
        c2_books_names = Documents_utils.get_list_of_docs_files(Documents_utils.c2)
        c3_books_names = Documents_utils.get_list_of_docs_files(Documents_utils.c3)

        c1_cluster = Embed_DataSet._embed_books_list(books_names_list=c1_books_names,
                                                     cluster_name='c1',
                                                     embedding_size=embedding_size,
                                                     tweet_size=tweet_size,
                                                     cluster_dir=Documents_utils.c1)

        c2_cluster = Embed_DataSet._embed_books_list(books_names_list=c2_books_names,
                                                     cluster_name='c2',
                                                     embedding_size=embedding_size,
                                                     tweet_size=tweet_size,
                                                     cluster_dir=Documents_utils.c2)

        c3_cluster = Embed_DataSet._embed_books_list(books_names_list=c3_books_names,
                                                     cluster_name='c3',
                                                     embedding_size=embedding_size,
                                                     tweet_size=tweet_size,
                                                     cluster_dir=Documents_utils.c3)

        return c1_cluster, c2_cluster, c3_cluster, c3_books_names

    @staticmethod
    def _embed_books_list(books_names_list, cluster_name, embedding_size, tweet_size, cluster_dir, main_array):
        embedded_book_list = []

        if embedding_size == 1024:
            embedded_books_names = []
            dir_path = Embed_book.get_book_cluster_dir_path(cluster_name)
            Embed_DataSet.get_clusters_sizes()
            for name in books_names_list:
                Embed_book.embed_book_and_save_1024(cluster_name=cluster_name,
                                                    file_name=name,
                                                    embedding_size=embedding_size,
                                                    tweet_size=tweet_size,
                                                    cluster_dir=cluster_dir)
                embedded_books_names.append(Embed_book.convert_file_name_to_embedded_name(file_name=name,
                                                                               embedding_size=embedding_size,
                                                                               tweet_size=tweet_size))

        if embedding_size == 300 or embedding_size == 100:
            for name in books_names_list:
                embedded_book_list.append(Embed_book.embed_book_AraVec(file_name=name,
                                                                       embedding_size=embedding_size,
                                                                       tweet_size=tweet_size,
                                                                       cluster_dir=cluster_dir))

        return embedded_book_list

    @staticmethod
    def check_for_missing_embedded_data_files(files_reg_names, cluster_name, embedding_size, tweet_size):
        """ Check if there is missing npy file that had been saved, if yes it return true, else false"""
        for file_name in files_reg_names:
            file_path = Embed_book.get_book_cluster_dir_path(cluster_name) + "\\" + \
                        Embed_book.convert_file_name_to_embedded_name(file_name, embedding_size, tweet_size)
            if not os.path.isfile(file_path):
                return True

        return False

    @staticmethod
    def get_clusters_sizes(embedded_books_names, dir_path):
        total_size = 0
        for embedded_book_name in embedded_books_names:
            file_path = dir_path + "\\" + embedded_book_name
            with open(file_path, 'rb') as f:
                major, minor = np.lib.format.read_magic(f)
                shape, fortran, dtype = np.lib.format.read_array_header_1_0(f)
                if len(shape) == 3:
                    total_size += shape[0]

        return total_size


if __name__ == "__main__":
    pass