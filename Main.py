import Algs.Embedding as Emb
import Algs.Embedd_DataSet as Emb_D
from utils.doc_utils import Documents_utils
import Objects.Book as Book
import numpy as np

# test for embedding class
books = Documents_utils.get_list_of_books(Documents_utils.c2)
books=books[:min(2,len(books))]
# clean_book = Emb.Embedding.clean_str(books[0])
# splited_word = clean_book.split()
# print(len(splited_word))

# result = Emb.Embedding.AraVec(splited_word)
# result = Emb.Embedding.Elmo(splited_word[:120])

# print(len(result))
# for vec in result:
#     print(vec)


# test for embedding DataSet class

# print("There is " + str(len(books))+" BOOKs")
# embedded_data = Emb_D.Embedd_DataSet.embedd_Elmo(books=books, tweet_size=100)
embedded_data = Emb_D.Embedd_DataSet.embedd_Aravec(books=books, tweet_size=100)
print(embedded_data.shape)
print("Test")

# index=0
# for book in books:
#     book_o = Book.Book(index,"x"+str(index), 0, book)
#     book_o.divide_book_to_paragraph()
#     book_o.process_book_statistics()
#     print(book_o.get_book_statistics())
#     index+=1


