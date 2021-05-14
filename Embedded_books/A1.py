import os

import numpy as np

from GUI.App.pages.process_bar import ProcessBar
from utils.doc_utils import Documents_utils
from Algs.Embedd_DataSet import Embedd_DataSet


class Embed_data_set:

    @staticmethod
    def embed_data_set(embedding_size, tweet_size, c1_dir: str, c2_dir: str, c3_dir: str, process: ProcessBar):
        # repeating code for c1, c2, c3

        c1_books_files_names_txt = Documents_utils.get_list_of_docs_files(c1_dir)
        c2_books_files_names_txt = Documents_utils.get_list_of_docs_files(c2_dir)
        c3_books_files_names_txt = Documents_utils.get_list_of_docs_files(c3_dir)

        if embedding_size == 1024:
            # repeating code for c1, c2, c3
            process.inc()
            process.status = 'Converting File Names of c1'
            c1_books_files_names_npy = Embed_data_set.convert_file_name_to_embedded_name(
                files_names=c1_books_files_names_txt,
                embedding_size=embedding_size,
                tweet_size=tweet_size)
            process.inc()
            process.status = 'Converting File Names of c2'
            c2_books_files_names_npy = Embed_data_set.convert_file_name_to_embedded_name(
                files_names=c2_books_files_names_txt,
                embedding_size=embedding_size,
                tweet_size=tweet_size)
            process.inc()
            process.status = 'Converting File Names of c3'

            c3_books_files_names_npy = Embed_data_set.convert_file_name_to_embedded_name(
                files_names=c3_books_files_names_txt,
                embedding_size=embedding_size,
                tweet_size=tweet_size)

            # embed the data and save it

            # repeating code for c1, c2, c3
            # c1
            process.inc()
            process.status = 'Save c1.npy '
            c1_embedded_books_cluster_dir = Embed_data_set.get_book_cluster_dir_path("c1")
            un_embedded_book_cluster_path = c1_dir
            for file_txt_name, file_npy_name in zip(c1_books_files_names_txt, c1_books_files_names_npy):
                Embed_data_set.embed_and_save_book_1024(embedded_file_name=file_npy_name,
                                                        embedded_books_cluster_dir=c1_embedded_books_cluster_dir,
                                                        curr_book_path=un_embedded_book_cluster_path + "\\" + file_txt_name,
                                                        tweet_size=tweet_size)
            # c2
            process.inc()
            process.status = 'Saving c2.npy'
            c2_embedded_books_cluster_dir = Embed_data_set.get_book_cluster_dir_path("c2")
            un_embedded_book_cluster_path = c2_dir
            for file_txt_name, file_npy_name in zip(c2_books_files_names_txt, c2_books_files_names_npy):
                Embed_data_set.embed_and_save_book_1024(embedded_file_name=file_npy_name,
                                                        embedded_books_cluster_dir=c2_embedded_books_cluster_dir,
                                                        curr_book_path=un_embedded_book_cluster_path + "\\" + file_txt_name,
                                                        tweet_size=tweet_size)



            # c3
            process.inc()
            process.status = 'Saving c3.npy'
            c3_embedded_books_cluster_dir = Embed_data_set.get_book_cluster_dir_path("c3")
            un_embedded_book_cluster_path = c3_dir
            for file_txt_name, file_npy_name in zip(c3_books_files_names_txt, c3_books_files_names_npy):
                Embed_data_set.embed_and_save_book_1024(embedded_file_name=file_npy_name,
                                                        embedded_books_cluster_dir=c3_embedded_books_cluster_dir,
                                                        curr_book_path=un_embedded_book_cluster_path + "\\" + file_txt_name,
                                                        tweet_size=tweet_size)

            # repeating code for c1, c2, c3
            # get total clusters sizes
            process.inc()
            process.status = 'Allocating the main array'
            c1_size, c1_embedded_books_array_length = Embed_data_set.get_cluster_size(c1_books_files_names_npy,
                                                                                      c1_embedded_books_cluster_dir)
            c2_size, c2_embedded_books_array_length = Embed_data_set.get_cluster_size(c2_books_files_names_npy,
                                                                                      c2_embedded_books_cluster_dir)
            # c3_size, c3_embedded_books_array_length = Embed_data_set.get_cluster_size(c3_books_files_names_npy,
            #                                                                           c3_embedded_books_cluster_dir)

            # create the main memory array
            # main_array = np.zeros((c1_size + c2_size + c3_size, tweet_size, embedding_size))
            main_array = np.zeros((c1_size + c2_size, tweet_size, embedding_size), dtype='f')

            # append the saved files to the main array
            # repeating code for c1, c2, c3
            process.inc()
            process.status = 'Loading the cluster to main array of c1'
            start_idx = 0
            begin_idx = 0
            start_idx = Embed_data_set.load_cluster_to_main_array(books_files_names_npy=c1_books_files_names_npy,
                                                                  embedded_cluster_dir=c1_embedded_books_cluster_dir,
                                                                  main_array=main_array,
                                                                  start_idx=start_idx,
                                                                  embedded_books_array_length=c1_embedded_books_array_length)

            c1_cluster = main_array[begin_idx: start_idx]
            begin_idx = start_idx
            process.inc()
            process.status = 'Loading the cluster to main array of c2'
            start_idx = Embed_data_set.load_cluster_to_main_array(books_files_names_npy=c2_books_files_names_npy,
                                                                  embedded_cluster_dir=c2_embedded_books_cluster_dir,
                                                                  main_array=main_array,
                                                                  start_idx=start_idx,
                                                                  embedded_books_array_length=c2_embedded_books_array_length)
            c2_cluster = main_array[begin_idx: start_idx]
            begin_idx = start_idx


            # start_idx = Embed_data_set.load_cluster_to_main_array(books_files_names_npy=c3_books_files_names_npy,
            #                                                       embedded_cluster_dir=c3_embedded_books_cluster_dir,
            #                                                       main_array=main_array,
            #                                                       start_idx=start_idx,
            #                                                       embedded_books_array_length=c3_embedded_books_array_length)
            # c3_cluster = main_array[begin_idx: start_idx]
            # begin_idx = start_idx
            process.inc()
            process.status = 'Loading the cluster to main array of c3'
            c3_cluster = []
            Embed_data_set.load_cluster(c3_cluster, c3_books_files_names_npy, c3_embedded_books_cluster_dir)
            process.inc()
            process.status = 'Finished'

            return c1_cluster, c2_cluster, c3_cluster, c3_books_files_names_txt, c1_size, c2_size


        elif embedding_size == 300 or embedding_size == 100:
            # just embed and save
            c1_cluster = []
            c2_cluster = []
            c3_cluster = []

            # c1
            un_embedded_book_cluster_path = Documents_utils.c1
            for file_txt_name in c1_books_files_names_txt:
                c1_cluster.append(Embed_data_set.embed_book_AraVec(
                    curr_book_path=un_embedded_book_cluster_path + "\\" + file_txt_name,
                    embedding_size=embedding_size,
                    tweet_size=tweet_size))

            # c2
            un_embedded_book_cluster_path = Documents_utils.c2
            for file_txt_name in c2_books_files_names_txt:
                c2_cluster.append(Embed_data_set.embed_book_AraVec(
                    curr_book_path=un_embedded_book_cluster_path + "\\" + file_txt_name,
                    embedding_size=embedding_size,
                    tweet_size=tweet_size))

            # c3
            un_embedded_book_cluster_path = Documents_utils.c3
            for file_txt_name in c3_books_files_names_txt:
                c3_cluster.append(Embed_data_set.embed_book_AraVec(
                    curr_book_path=un_embedded_book_cluster_path + "\\" + file_txt_name,
                    embedding_size=embedding_size,
                    tweet_size=tweet_size))

            return c1_cluster, c2_cluster, c3_cluster, c3_books_files_names_txt

        raise Exception("invalid embedding_size" + str(embedding_size))

    @staticmethod
    def embed_and_save_book_1024(embedded_file_name, embedded_books_cluster_dir, curr_book_path, tweet_size):

        book_embedding_path = embedded_books_cluster_dir + "\\" + embedded_file_name
        # check if file exist
        if os.path.exists(book_embedding_path):
            return

        # there is No prev embedded book
        # load the text file
        embedded_data = Embedd_DataSet.embedd_Elmo(books=[Documents_utils.read_doc_file(curr_book_path)],
                                                   tweet_size=tweet_size)

        # save the file
        # check if dir exist
        if not os.path.isdir(embedded_books_cluster_dir):
            os.mkdir(embedded_books_cluster_dir)

        np.save(book_embedding_path, embedded_data)
        return

    @staticmethod
    def embed_book_AraVec(curr_book_path, embedding_size, tweet_size):
        return Embedd_DataSet.embedd_Aravec(books=[Documents_utils.read_doc_file(curr_book_path)],
                                            tweet_size=tweet_size,
                                            embedding_dimension=embedding_size)

    @staticmethod
    def load_cluster_to_main_array(books_files_names_npy, embedded_cluster_dir, main_array, start_idx,
                                   embedded_books_array_length):
        for idx, book_file_name in enumerate(books_files_names_npy):
            start_idx = Embed_data_set.load_npy_file_append_to_main_matrix(
                file_path=embedded_cluster_dir + "\\" + book_file_name,
                main_array=main_array,
                start_idx=start_idx,
                length=embedded_books_array_length[idx])

        return start_idx

    @staticmethod
    def load_cluster(c3_cluster, books_files_names_npy, embedded_cluster_dir):
        for book_name in books_files_names_npy:
            file_path = embedded_cluster_dir + "\\" + book_name
            c3_cluster.append(np.load(file_path))

    @staticmethod
    def load_npy_file_append_to_main_matrix(file_path, main_array, start_idx, length):
        """ merge a numpy array to the main array and return the updated idx"""
        main_array[start_idx: start_idx + length] = np.load(file_path)
        return start_idx + length

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

    @staticmethod
    def get_cluster_size(embedded_books_names, dir_path):
        total_size = 0
        each_book_size = []
        for embedded_book_name in embedded_books_names:
            file_path = dir_path + "\\" + embedded_book_name
            with open(file_path, 'rb') as f:
                major, minor = np.lib.format.read_magic(f)
                shape, fortran, dtype = np.lib.format.read_array_header_1_0(f)
                if len(shape) == 3:
                    total_size += shape[0]
                    each_book_size.append(shape[0])

        return total_size, each_book_size
