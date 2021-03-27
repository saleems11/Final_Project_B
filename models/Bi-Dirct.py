from random import random

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer

import random as rnd
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

def make_prediction(data):
    prediction_res = np.zeros(shape=(2,))
    predictions = model.predict(data)
    for prediction in predictions:
        prediction_res = np.add(prediction_res, prediction)

    return prediction_res/len(data)



def test_model(anchor_c1, anchor_c2, c3):
    # return numpy array

    # predict the anchor data and the c3
    c1_prediction = []
    c2_prediction = []
    for i in range(0, len(anchor_c1)):
        prediction_c1 = make_prediction(anchor_c1[i])
        c1_prediction.append(prediction_c1)

    for i in range(0, len(anchor_c2)):
        prediction_c2 = make_prediction(anchor_c2[i])
        c2_prediction.append(prediction_c2)

    c1_prediction = np.array(c1_prediction, dtype='f')
    c2_prediction = np.array(c2_prediction, dtype='f')

    # prediction for each book
    c3_prediction = []
    for i in range(0, len(c3)):
        prediction_c3 = make_prediction(c3[i])
        c3_prediction.append(prediction_c3)

    c3_prediction = np.array(c3_prediction, dtype='f')

    prediction_t = np.concatenate((c1_prediction, c2_prediction), axis=0)
    prediction_t = np.concatenate((prediction_t, c3_prediction), axis=0)

    return prediction_t


def train_model_itteration(model, c1, c2, anchor_c1, anchor_c2, c3, epoch, batch_size, itterations):
    results = []
    M = []

    for _ in range(itterations):
        x_train, y_train = create_new_batch(c1, c2)
        history = model.fit(x_train, y_train, validation_split=.30, epochs=epoch, batch_size=batch_size, verbose=1)

        # test the model
        M.append(test_model(anchor_c1, anchor_c2, c3))

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

    return results, history, M


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
    c1 = c1[:min(44, len(c1))]
    c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
    c2 = c2[:min(20, len(c2))]
    c3 = Documents_utils.get_list_of_books(Documents_utils.c3)
    c3 = c3[:min(1, len(c3))]


    # the anchor data set
    anchor_index_c1 = rnd.sample(range(len(c1)), 7)
    anchor_index_c2 = rnd.sample(range(len(c2)), 2)
    anchor_index_c1.sort()
    anchor_index_c2.sort()

    anchor_c1 = []
    anchor_c2 = []

    # remove from c1, c2 the anchor books, and create anchor books list
    for i in range(0, len(anchor_index_c1)):
        anchor_c1.append(c1[anchor_index_c1[i]])

    for i in range(0, len(anchor_index_c2)):
        anchor_c2.append(c2[anchor_index_c2[i]])

    for i in range(0, len(anchor_index_c1)):
        c1.pop(anchor_index_c1[i]-i)

    for i in range(0, len(anchor_index_c2)):
        c2.pop(anchor_index_c2[i]-i)

    embedded_anchor_c1 = []
    embedded_anchor_c2 = []
    embedded_data_c3 = []

    if embedding_size == 1024:
        embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=tweet_size)
        embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=tweet_size)

        for i in range(0, len(c3)):
            embedded_data_c3.append(Emb_D.Embedd_DataSet.embedd_Elmo(books=c3[i], tweet_size=tweet_size))

        for i in range(len(anchor_c1)):
            embedded_anchor_c1.append(Emb_D.Embedd_DataSet.embedd_Elmo(books=anchor_c1[i], tweet_size=tweet_size))

        for i in range(len(anchor_c2)):
            embedded_anchor_c2.append(Emb_D.Embedd_DataSet.embedd_Elmo(books=anchor_c2[i], tweet_size=tweet_size))


    if embedding_size == 300 or embedding_size == 100:
        embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=tweet_size, embedding_dimension=embedding_size)
        embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=tweet_size, embedding_dimension=embedding_size)

        # get embedding for each book
        embedded_data_c3 = []
        embedded_anchor_c2 = []
        embedded_anchor_c1 = []
        for i in range(0, len(c3)):
            embedded_data_c3.append(Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([c3[i], ]), tweet_size=tweet_size, embedding_dimension=embedding_size))

        for i in range(len(anchor_c1)):
            embedded_anchor_c1.append(Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([anchor_c1[i], ]), tweet_size=tweet_size, embedding_dimension=embedding_size))

        for i in range(len(anchor_c2)):
            embedded_anchor_c2.append(Emb_D.Embedd_DataSet.embedd_Aravec(books=np.array([anchor_c2[i], ]), tweet_size=tweet_size, embedding_dimension=embedding_size))

    return embedded_data_c1, embedded_data_c2, embedded_data_c3, embedded_anchor_c1, embedded_anchor_c2


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
drop_out = 0.4
learning_rate = 0.001
epoch = 23
batch_size = 100
itterations = 2
fully_connected_layer = 30

# file for saving the result and the parameters
file = open("result_checks.txt", "a")

# the data need to be normalized
c1, c2, c3, anchor_c1, anchor_c2 = load_data(tweet_lenght, embedding_size)

model = create_model(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                     tweet_lenght=tweet_lenght,
                     embedding_size=embedding_size,
                     drop_out=drop_out,
                     fully_connected_layer=fully_connected_layer,
                     learning_rate=learning_rate)

results, history, M = train_model_itteration(model=model, c1=c1, c2=c2, anchor_c1=anchor_c1,
                                             anchor_c2=anchor_c2, c3=c3, epoch=epoch, batch_size=batch_size, itterations=itterations)


for result in results:
    result.plot()

plt.show()

# the K-means
M = np.concatenate(M, axis=0)
print(M)
kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=100, random_state=42)
labels = kmeans.fit_predict(M)



plt.scatter(M[:, 0], M[:, 1], c=labels, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.3)
plt.show()

score = silhouette_score(M, labels=labels, metric='euclidean')
print("The Silhouette score is :"+str(score))

file.write("-- tweet len:{0}, epochs:{1}, batch_size={2}, drop_out={3}, bi_lstm_hidden_state_size:{4}"
           "\naccuracy:{5}, validation accuracy: {6}, learning rate: {7}, embedding_size: {8}\n"
           "The Silhouette score: {9}\n".format(
    tweet_lenght, epoch, batch_size, drop_out,
    bi_lstm_hidden_state_size, sum(history.history['accuracy']) / len(history.history['accuracy'])
    , sum(history.history['val_accuracy']) / len(history.history['val_accuracy']), learning_rate, embedding_size,
    score))
file.close()


visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')
visualizer.fit(M)
visualizer.show()