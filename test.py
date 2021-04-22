# import torch
#
# print(torch.__version__)
# print(torch.cuda.is_available())
# print(torch.version.cuda)
#
# import Tests.send_mail as SM
# SM.send_mail("iamme0ssa@gmail.com", "Al-Ghazali project","Error occurred, trying to run again")
#
# print("hello {0}".format(round(0.8199999928474426, 2)))


# import numpy as np
#
# lst = []
#
# lst.append(np.zeros((2,4,2), dtype='f'))
# lst.append(np.zeros((3,4,2), dtype='f'))
#
# nw = np.concatenate( lst, axis=0 )
# print(nw.shape)
# print(nw)
# np.save('a.npy', lst, allow_pickle=True)
# b = np.load('a.npy', allow_pickle=True)
#
# for x in b:
#     print(x.shape)
# print("hero")
# x = "hello.tct"
# print(x[:-4])

from pandas import DataFrame
import pandas as pd

lst = [[1, 2], [2, 2]]
names = ['accuracy', 'loss']
new_lst = DataFrame()
temp = DataFrame()
for i in range(len(lst)):
    new_lst[names[i]] = lst[i]
    temp[names[i]] = lst[i]

new_lst = new_lst.append(temp, ignore_index=True)
print(new_lst.head(10))
