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

for i in range(5):
    lst.append(np.zeros((2,4), dtype='f'))

np.save('a.npy', np.array(lst, dtype='f'))
