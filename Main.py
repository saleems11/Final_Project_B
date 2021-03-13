import Algs.Embedding as Emb
from utils.doc_utils import Documents_utils

book = Documents_utils.get_list_of_books(Documents_utils.c1)[0]
clean_book = Emb.Embedding.clean_str(book)
splited_word = clean_book.split()
print(len(splited_word))

# result = Emb.Embedding.AraVec(splited_word)
result = Emb.Embedding.Elmo(splited_word)

print(len(result))
# for vec in result:
#     print(vec)
