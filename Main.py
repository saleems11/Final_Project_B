import Algs.Embedding as Emb
import Algs.Embedd_DataSet as Emb_D
from utils.doc_utils import Documents_utils

books = Documents_utils.get_list_of_books(Documents_utils.c1)
books=books[:min(2,len(books))]
# clean_book = Emb.Embedding.clean_str(book)
# splited_word = clean_book.split()
# print(len(splited_word))

# result = Emb.Embedding.AraVec(splited_word)
# result = Emb.Embedding.Elmo(splited_word)

# print(len(result))
# for vec in result:
#     print(vec)

print("There is " + str(len(books))+" BOOKs")
# embedded_data = Emb_D.Embedd_DataSet.embedd_Elmo(books=books, tweet_size=32)
embedded_data = Emb_D.Embedd_DataSet.embedd_Aravec(books=books, tweet_size=32)
print("Test")
