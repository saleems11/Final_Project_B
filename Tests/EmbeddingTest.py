import unittest

import Algs.Embedding as Emb
from utils.doc_utils import Documents_utils

class TestEmbedding(unittest.TestCase):

    def test_AraVecEmbedding_c1(self):
        c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
        # self.c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
        # self.c3 = Documents_utils.get_list_of_books(Documents_utils.c3)

        clean_book = Emb.Embedding.clean_str(c1[0])
        splited_word = clean_book.split()
        result = Emb.Embedding.AraVec(splited_word)

        self.assertNotEqual(len(result), 0, "No")
        
    def test_ElmoEmbedding_c1(self):
        c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
        # self.c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
        # self.c3 = Documents_utils.get_list_of_books(Documents_utils.c3)

        clean_book = Emb.Embedding.clean_str(c1[0])
        splited_word = clean_book.split()
        result = Emb.Embedding.Elmo(splited_word[:120])

        self.assertEqual(result.shape, (1,), "No")

if __name__ == '__main__':
    unittest.main()