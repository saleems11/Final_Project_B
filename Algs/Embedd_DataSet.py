
import Algs.Embedding as Embedding
import numpy as np
import torch

class Embedd_DataSet:

    @staticmethod
    def embedd_Aravec(books:[str], tweet_size: int, embedding_dimension=100, epselon=0.001)->[[[[int]]]]:
        """Take the data and return the embedded result using AraVec
        The Embedding is applied at each book as one (word by word), and then the results of the embedding
         are divided into tweets and each tweet in size of tweet size words
        :parameter
        books:[str] array of books text
        tweet_size:int tweet size in words
        embedding_dimension: (100[default], 300)
        :returns
        Array of vector arrays for all the books"""
        embedded_DataSet=[]

        for book in books:
            clean_book = Embedding.Embedding.clean_str(book)
            splited_word = clean_book.split()

            emb_Data = Embedding.Embedding.AraVec(splited_word,embedding_dimension)
            # to reduce memory usage
            emb_Data = emb_Data.astype(dtype='f')

            for i in range(0, len(emb_Data), tweet_size):
                if i + tweet_size > len(emb_Data):
                    last = np.zeros(shape=((i + tweet_size)-len(emb_Data), embedding_dimension))
                    last = np.append(emb_Data[i:len(emb_Data)], last, axis= 0)
                    embedded_DataSet.append(last)
                else:
                    embedded_DataSet.append(emb_Data[i:i+tweet_size])



        result = np.empty(shape=(len(embedded_DataSet),
                                 len(embedded_DataSet[0]),
                                 len(embedded_DataSet[0][0])))

        for i,tweet in enumerate(embedded_DataSet):
            result[i]=tweet

        return result



    @staticmethod
    def embedd_Elmo(books: [str], tweet_size: int, epselon=0.001)->[[ [[int]]]]:
        """Embedding using Elmo, the book is divided into tweets and each tweet in size of tweet size words
        and then feed into Elmo one book at a time, each book containing many tweets, each tweet contain
        several words, and each word is embedded into a vector
        :parameter
        books:[str] array of books text
        tweet_size:int tweet size in words
        :returns
        embedded_DataSet: where it contain each book embedding as a matrix of (tweets amount,  embedding dim)
        """
        embedded_DataSet = []

        for index, book in enumerate(books):
            clean_book = Embedding.Embedding.clean_str(book)
            splited_word = clean_book.split()

            tweets=[]
            for i in range(0, len(splited_word), tweet_size):
                if i + tweet_size > len(splited_word):
                    last = [""] * ((i + tweet_size) - len(splited_word))
                    last.extend(splited_word[i: len(splited_word)])
                    tweets.append(last)
                else:
                    tweets.append(splited_word[i: i+tweet_size])

            embedded_DataSet.extend(Embedding.Embedding.Elmo(tweets))
            print("Book with index {0} had finished embedding".format(index))

        # to reduce memory usage
        embedded_DataSet = np.array(embedded_DataSet, dtype='f')

        # to reduce GPU cache memory used by torch
        torch.cuda.empty_cache()

        return embedded_DataSet
