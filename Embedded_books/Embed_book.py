import numpy as np
import os.path

from Algs.Embedd_DataSet import Embedd_DataSet
from Embedded_books.Embed_dataSet import Documents_utils


class Embed_book:

    @staticmethod
    def embed_book(cluster_name, file_name, embedding_size, tweet_size, cluster_dir):

        curr_book_path = os.path.join(cluster_dir, file_name)

        if embedding_size == 1024:
            # embed using Elmo

            embedded_file_name = '{0}_{1}.npy'.format(file_name[:-4], embedding_size)
            books_cluster_dir = "\\".join(
                [Documents_utils.project_working_dir, "Embedded_books", cluster_name])
            book_embedding_path = books_cluster_dir + "\\" + embedded_file_name
            # check if file exist
            if os.path.isfile(book_embedding_path):
                # load the file and return it
                return np.load(book_embedding_path)

            # there is No prev embedded book
            # load the text file
            embedded_data = Embedd_DataSet.embedd_Elmo(books=[Documents_utils.read_doc_file(curr_book_path)],
                                                       tweet_size=tweet_size)

            # save the file
            # check if dir exist
            if not os.path.isdir(books_cluster_dir):
                os.mkdir(books_cluster_dir)

            np.save(book_embedding_path, embedded_data)
            return embedded_data

        elif embedding_size == 300 or embedding_size == 100:
            # embed using AraVec
            return Embedd_DataSet.Embedd_DataSet.embedd_Aravec(books=[Documents_utils.read_doc_file(curr_book_path)],
                                                               tweet_size=tweet_size,
                                                               embedding_dimension=embedding_size)

        raise Exception("invalid embedding_size"+str(embedding_size))
