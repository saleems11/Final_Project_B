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


import numpy as np

lst = []

lst.append(np.zeros((2,4), dtype='f'))
lst.append(np.zeros((3,4), dtype='f'))

np.save('a.npy', lst, allow_pickle=True)
b = np.load('a.npy', allow_pickle=True)

for x in b:
    print(x.shape)
print("hero")