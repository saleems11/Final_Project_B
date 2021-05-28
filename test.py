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

# lst = [[1, 2], [2, 2]]
# names = ['accuracy', 'loss']
# new_lst = DataFrame()
# temp = DataFrame()
# for i in range(len(lst)):
#     new_lst[names[i]] = lst[i]
#     temp[names[i]] = lst[i]
#
# new_lst = new_lst.append(temp, ignore_index=True)
# print(new_lst.head(10))


# from Objects.SmartChecking import SmartChecking
#
# smartChecking = SmartChecking()
#
# for i in range(100):
#     smartChecking.new_parameters_values()


# import numpy as np
#
# ar = np.array([[1, 2], [2, 1]])
# fill = np.zeros((10, 2))
# fill[0:0+ar.shape[0]] = ar
# print(fill)

# lst = [1, 2]
# dst = [4, 5]
#
# for x,y in zip(lst, dst):
#     print(str(x) + ", " + str(y))

# a = {'a':'abc', 'b':'xyz'}
# print(a['a'])

# import numpy as np
#
# a = np.array([1, 2, 5, 10])
#
# print(a.max())

# from Objects.Book import Book
#
# a= []
# a.append(Book(0,0,0))
#
# for book in a:
#     book.add_label(0)
#
# print(a[0].label)

# import numpy as np
#
# a = np.array([1,2,3])
# print(np.divide(a, 2))

# def hel():
#     print("hello")
#
# def res(func):
#     func()
#     print("Done func")
#
# res(hel)

# book_name = 'me'
# cluster = 'c1'
# index = 0
# print("{0}({1})[{2}]".format(book_name, cluster, index))

a = list(range(10))
print(a)
