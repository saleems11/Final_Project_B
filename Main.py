import Algs.Embedding as Emb

book="سليم اكل التفاح وكان طعمه فظيع"
clean_book = Emb.Embedding.clean_str(book)
splited_word = clean_book.split()
result = Emb.Embedding.AraVec(splited_word)

# result = Emb.Embedding.Elmo(splited_word)
#
print(len(result))
# for vec in result:
#     print(vec)
