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




from keras.models import Sequential
from keras.models import Model
from keras.layers import LSTM, Conv2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import GlobalMaxPooling2D, Reshape, Permute, Concatenate
from keras.layers import Bidirectional

from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt

import models.LoadingBalancingData.DataManagement as DM
import Objects.TestingData as TD

"""Create a Bi-Direct LSTM model that is specified according to the parameters, and return the model.\n
The model have 5 layers(Bi-direct(LSTM)[the result are concat], DropOut, fully connected layer, DropOut,
softMax).\n
(for the LSTM model there is a need to reset the hidden and cell state after
each epoch and that is done when creating the model with the parameter stateful=False)"""

words_combination_len = 5
filters = 64
embedding_size = 1024
tweet_length = 200
bi_lstm_hidden_state_size = 96
drop_out = 0.3
fully_connected_layer = 30
learning_rate = 0.004
loss_func = 'binary_crossentropy'

""" Multi kernel sizes"""
model = Sequential()
# input_layer = tf.keras.Input(shape=(tweet_length, embedding_size, 1))
sub_models = []
for kw in (3, 4, 5):  # kernel sizes
    submodel = Sequential()
    submodel.add(Conv2D(filters=filters, kernel_size=(kw, embedding_size), padding="valid",
                        activation="relu", input_shape=(tweet_length, embedding_size, 1)))
    sub_models.append(submodel)
    # submodel.add(GlobalMaxPooling2D())
    # submodel.add(Reshape((model.output_shape[1], model.output_shape[3])))
    # submodel.add(Permute((2, 1)))

model.add(Concatenate(sub_models))
print(model.output_shape)
# input is None tweets, the model will be applied to each tweet of shape tweet_len, embedding_size => 200, 1024
# then the CNN will be applied to to multiple words together
# model.add(
#     Conv2D(filters=filters, kernel_size=(words_combination_len, embedding_size), padding="valid",
#            activation="relu", input_shape=(tweet_length, embedding_size, 1)))
#
model.add(Reshape((model.output_shape[1], model.output_shape[3])))
model.add(Permute((2, 1)))
# result shape (tweet_length - 10 + 1)/stride, filters=32

# model.add(MaxPooling2D(pool_size=(10, embedding_size)))

model.add(Bidirectional(
    LSTM(units=bi_lstm_hidden_state_size, return_sequences=False, stateful=False),
    merge_mode="concat"))

model.add(Dropout(drop_out))
model.add(Dense(fully_connected_layer, activation='relu'))
model.add(Dropout(drop_out))
model.add(Dense(2, activation='softmax'))

print(model.summary())
# # opt = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.95, decay=0.01)
# opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
# model.compile(loss=loss_func, optimizer=opt, metrics=['accuracy'])
#
# return model


