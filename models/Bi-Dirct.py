from random import random

import numpy as np
from numpy import array
from numpy import cumsum
from matplotlib import pyplot

import matplotlib.pyplot as plt
from pandas import DataFrame

import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import TimeDistributed
from keras.layers import Bidirectional

import Algs.Embedd_DataSet as Emb_D
from utils.doc_utils import Documents_utils
import Algs.Balancing_Routine as BR

# to run on the GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)


def train_model_itteration(model, c1, c2, epoch, batch_size, itterations):
    results = []

    for _ in range(itterations):
        x_train, y_train = create_new_batch(c1, c2)
        history = model.fit(x_train, y_train, validation_split=.30, epochs=epoch, batch_size=batch_size, verbose=1)

        result = DataFrame()
        accuracy = list()
        val_accuracy = list()
        loss = list()
        validation_loss = list()

        for i in range(0, len(history.history['accuracy'])):
            accuracy.append(history.history['accuracy'][i])
            val_accuracy.append(history.history['val_accuracy'][i])
            loss.append(history.history['loss'][i])
            validation_loss.append(history.history['val_loss'][i])

        result['accuracy'] = accuracy
        result['val_accuracy'] = val_accuracy
        result['loss'] = loss
        result['val_loss'] = validation_loss

        results.append(result)

    return results, history


def create_model(bi_lstm_hidden_state_size, tweet_lenght, embedding_size, drop_out, fully_connected_layer,
                 learning_rate):
    model = Sequential()
    model.add(Bidirectional(
        LSTM(units=bi_lstm_hidden_state_size, return_sequences=False),
        input_shape=(tweet_lenght, embedding_size),
        merge_mode="concat"))

    model.add(Dropout(drop_out))
    model.add(Dense(fully_connected_layer, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(2, activation='softmax'))

    print(model.summary())
    opt = tf.keras.optimizers.Adam(learning_rate=learning_rate, )
    model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])

    return model


def load_data(tweet_size, embedding_size):
    c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
    c1 = c1[:min(50, len(c1))]
    c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
    c2 = c2[:min(10, len(c2))]
    c3 = Documents_utils.get_list_of_books(Documents_utils.c3)
    c3 = c2[:min(1, len(c3))]

    # embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=tweet_size)
    embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=tweet_size, embedding_dimension=embedding_size)
    print(embedded_data_c1.shape)

    # embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=tweet_size)
    embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=tweet_size, embedding_dimension=embedding_size)
    print(embedded_data_c2.shape)

    # embedded_data_c3 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c3, tweet_size=tweet_size)
    embedded_data_c3 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c3, tweet_size=tweet_size, embedding_dimension=embedding_size)
    print(embedded_data_c3.shape)

    return embedded_data_c1, embedded_data_c2, embedded_data_c3


def create_new_batch(embedded_data_c1, embedded_data_c2):
    # Now lets balance the data
    s1, s2 = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
                                                    embedded_data_c2,
                                                    3,
                                                    2)

    x_train = np.concatenate((s1, s2))
    # the first value is gazali, the sec is psedo
    y1 = np.tile(np.array([1, 0]), (len(s1), 1))
    y2 = np.tile(np.array([0, 1]), (len(s2), 1))
    y_train = np.concatenate((y1, y2))

    # Random permutation
    p = np.random.permutation(len(x_train))
    x_train = x_train[p]
    y_train = y_train[p]

    return x_train, y_train


# parameters
embedding_size = 300
tweet_lenght = 200
bi_lstm_hidden_state_size = 50
drop_out = 0.3
learning_rate = 0.0001
epoch = 25
batch_size = 100
itterations = 2
fully_connected_layer = 10

# file for saving the result and the parameters
file = open("result_checks.txt", "a")

# the data need to be normlized
c1, c2, c3 = load_data(tweet_lenght, embedding_size)

model = create_model(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                     tweet_lenght=tweet_lenght,
                     embedding_size=embedding_size,
                     drop_out=drop_out,
                     fully_connected_layer=fully_connected_layer,
                     learning_rate=learning_rate)

results, history = train_model_itteration(model=model, c1=c1, c2=c2, epoch=epoch,
                                          batch_size=batch_size, itterations=itterations)

file.write("-- tweet len:{0}, epochs:{1}, batch_size={2}, drop_out={3}, bi_lstm_hidden_state_size:{4}"
           "\naccuracy:{5}, validation accuracy: {6}, learning rate: {7}, embedding_size: {8}\n".format(
    tweet_lenght, epoch, batch_size, drop_out,
    bi_lstm_hidden_state_size, sum(history.history['accuracy']) / len(history.history['accuracy'])
    , sum(history.history['val_accuracy']) / len(history.history['val_accuracy']), learning_rate, embedding_size))
file.close()

for result in results:
    result.plot()

plt.show()
