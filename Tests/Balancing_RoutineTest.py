import Algs.Embedding as Emb
import Algs.Embedd_DataSet as Emb_D
from utils.doc_utils import Documents_utils
import numpy as np
import Algs.Balancing_Routine as BR

print("Test")

c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
c1=c1[:min(3,len(c1))]
c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
c2=c2[:min(1,len(c1))]


# embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=100)
embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=100)
print(embedded_data_c1.shape)


# embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=100)
embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=100)
print(embedded_data_c2.shape)

# Now lets balance the data
s1,s2 = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
                                       embedded_data_c2,
                                       3,
                                       3)


print("C1 -shape after balancing ={0}, before balancing ={1}".format(str(s1.shape),
                                                                 str(embedded_data_c1.shape)))
print("C2 -shape after balancing ={0}, before balancing ={1}".format(str(s2.shape),
                                                                 str(embedded_data_c2.shape)))

