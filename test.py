import numpy as np


x = np.array([[1., 0.], [2., 1.], [0., 0.]])
y = np.array([0, 1, 2])
p = np.random.permutation(len(x))
x = x[p]
y = y[p]
print("Finish")