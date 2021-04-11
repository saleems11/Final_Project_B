from utils.doc_utils import Documents_utils
from Embedded_books.Embed_book import Embed_book


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

        return c1_cluster, c2_cluster, c3_cluster

    @staticmethod
    def _embed_books_list(books_names_list, cluster_name, embedding_size, tweet_size, cluster_dir):
        embedded_book_list = []
        for name in books_names_list:
            embedded_book_list.append(Embed_book.embed_book(cluster_name=cluster_name,
                                                            file_name=name,
                                                            embedding_size=embedding_size,
                                                            tweet_size=tweet_size,
                                                            cluster_dir=cluster_dir))
        return embedded_book_list
