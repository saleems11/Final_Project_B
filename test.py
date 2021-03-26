import numpy as np


a = []
a.append([5,6])
a.append([1,2])
a = np.array(a, dtype='f')

print(np.concatenate( a, axis=0))

# x = np.array([[1, 0], [2, 1], [0, 0]])
# y = np.array([0, 1, 2])
# p = np.random.permutation(len(x))
# x = x[p]
# y = y[p]
print("Finish")