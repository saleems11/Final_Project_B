# import torch
#
# print(torch.__version__)
# print(torch.cuda.is_available())
# print(torch.version.cuda)

import random

for i in range(100):
    if random.randint(0,10) == 10:
        print("BUG in my code")