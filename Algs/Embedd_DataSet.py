
import Algs.Embedding as Embedding
import numpy as np

class Embedd_DataSet:

    @staticmethod
    def embedd_Aravec(books:[str], tweet_size: int, embedding_dimension = 100)->[[[[int]]]]:
        """Take the data and return the embedded result using AraVec\n
        The collection of books as array of string array, embed_dim could be choosed
        (100[default], 300):parameter\n
        Array of vector arrays for all the books:returns\n"""
        embedded_DataSet=[]

        for book in books:
            clean_book = Embedding.Embedding.clean_str(book)
            splited_word = clean_book.split()

            emb_Data = Embedding.Embedding.AraVec(splited_word,embedding_dimension)

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
    def embedd_Elmo(books: [str], tweet_size: int)->[[ [[int]]]]:
        """for Now each book is divided into tweets\n
        there is need to check if the model is trained on tweets or data batches
        and what the effect of l and l0\n
        :parameter\n
        array in size of number of books, divided into tweets
        , each tweet contain several words, and each word is embedded into a vector:returns\n"""
        embedded_DataSet = []

        for book in books:
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

        return np.array(embedded_DataSet)
