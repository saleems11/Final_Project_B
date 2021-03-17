from random import random

import numpy as np
from numpy import array
from numpy import cumsum
from matplotlib import pyplot

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
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)






def train_model(model, x_train, y_train,itterations):
	loss = list()
	for _ in range(itterations):

		# fit model for one epoch on this sequence
		hist = model.fit(x_train, y_train, epochs=10, batch_size=50, verbose=0)
		loss.append(hist.history['loss'][0])
	return loss



def load_data():
	c1 = Documents_utils.get_list_of_books(Documents_utils.c1)
	c1 = c1[:min(3, len(c1))]
	c2 = Documents_utils.get_list_of_books(Documents_utils.c2)
	c2 = c2[:min(1, len(c2))]
	c3 = Documents_utils.get_list_of_books(Documents_utils.c3)
	c3 = c2[:min(1, len(c3))]

	# embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c1, tweet_size=100)
	embedded_data_c1 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c1, tweet_size=100)
	print(embedded_data_c1.shape)

	# embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c2, tweet_size=100)
	embedded_data_c2 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c2, tweet_size=100)
	print(embedded_data_c2.shape)

	# embedded_data_c3 = Emb_D.Embedd_DataSet.embedd_Elmo(books=c3, tweet_size=100)
	embedded_data_c3 = Emb_D.Embedd_DataSet.embedd_Aravec(books=c3, tweet_size=100)
	print(embedded_data_c3.shape)

	# Now lets balance the data
	s1, s2 = BR.Balancing_DataSet.Balancing_Routine(embedded_data_c1,
													embedded_data_c2,
													3,
													2)
	return s1,s2,c3


embedding_size= 100
tweet_lenght = 100
# the data need to be normlized
s1,s2,c3 = load_data()
x_train = np.concatenate((s1,s2))
# the first value is gazali, the sec is psedo
y1 = np.tile(np.array([1,0]),(len(s1),1))
y2 = np.tile(np.array([0,1]),(len(s2),1))
y_train = np.concatenate((y1,y2))

x_test = c3



""" creatin the model"""
bi_lstm_hidden_state_size = 200

model = Sequential()
model.add(Bidirectional(
	LSTM(units=bi_lstm_hidden_state_size, return_sequences=False),
	input_shape=(tweet_lenght, embedding_size),
	merge_mode="concat"))

model.add(Dropout(0.2))
model.add(Dense(2*bi_lstm_hidden_state_size, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2, activation='relu'))

print(model.summary())
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, batch_size=50, verbose=0)

results = DataFrame()
# results['bilstm_con'] = train_model(model, x_train, y_train, 20)
# line plot of results
# results.plot()
# pyplot.show()