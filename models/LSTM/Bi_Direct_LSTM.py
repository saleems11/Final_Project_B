import tensorflow as tf
from keras.models import Sequential
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


class Bi_Direct_LSTM:

    def __init__(self, bi_lstm_hidden_state_size, tweet_length, embedding_size, drop_out, fully_connected_layer,
                 learning_rate, loss_func):
        # to run on the GPU and solve a bug
        gpu_devices = tf.config.experimental.list_physical_devices('GPU')
        for device in gpu_devices:
            tf.config.experimental.set_memory_growth(device, True)

        self.bi_lstm_hidden_state_size = bi_lstm_hidden_state_size
        self.tweet_length = tweet_length
        self.embedding_size = embedding_size
        self.drop_out = drop_out
        self.fully_connected_layer = fully_connected_layer
        self.learning_rate = learning_rate
        self.loss_func = loss_func

        self.model = Bi_Direct_LSTM.create_model(bi_lstm_hidden_state_size, tweet_length, embedding_size, drop_out,
                                                 fully_connected_layer, learning_rate, loss_func)

    @staticmethod
    def create_model(bi_lstm_hidden_state_size, tweet_length, embedding_size, drop_out, fully_connected_layer,
                     learning_rate, loss_func='binary_crossentropy'):
        """Create a Bi-Direct LSTM model that is specified according to the parameters, and return the model.\n
        The model have 5 layers(Bi-direct(LSTM)[the result are concat], DropOut, fully connected layer, DropOut,
        softMax).\n
        (for the LSTM model there is a need to reset the hidden and cell state after
        each epoch and that is done when creating the model with the parameter stateful=False)"""

        words_combination_len = 5
        filters = 64

        """ Multi kernel sizes"""
        submodels = []
        for kw in (3, 4, 5):  # kernel sizes
            submodel = Sequential()
            submodel.add(Conv2D(filters=filters, kernel_size=(kw, embedding_size), padding="valid",
                                activation="relu", input_shape=(tweet_length, embedding_size, 1)))
            # submodel.add(GlobalMaxPooling2D())
            # submodel.add(Reshape((model.output_shape[1], model.output_shape[3])))
            # submodel.add(Permute((2, 1)))
            submodels.append(submodel)

        big_model = Sequential()
        big_model.add(Concatenate(submodels))

        # input is None tweets, the model will be applied to each tweet of shape tweet_len, embedding_size => 200, 1024
        # then the CNN will be applied to to multiple words together
        # model.add(
        #     Conv2D(filters=filters, kernel_size=(words_combination_len, embedding_size), padding="valid",
        #            activation="relu", input_shape=(tweet_length, embedding_size, 1)))
        #
        big_model.add(Reshape((big_model.output_shape[1], big_model.output_shape[3])))
        big_model.add(Permute((2, 1)))
        # result shape (tweet_length - 10 + 1)/stride, filters=32

        # model.add(MaxPooling2D(pool_size=(10, embedding_size)))

        big_model.add(Bidirectional(
            LSTM(units=bi_lstm_hidden_state_size, return_sequences=False, stateful=False),
            input_shape=(tweet_length, embedding_size),
            merge_mode="concat"))

        big_model.add(Dropout(drop_out))
        big_model.add(Dense(fully_connected_layer, activation='relu'))
        big_model.add(Dropout(drop_out))
        big_model.add(Dense(2, activation='softmax'))

        print(big_model.summary())
        # opt = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.95, decay=0.01)
        opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        big_model.compile(loss=loss_func, optimizer=opt, metrics=['accuracy'])

        return big_model

    @staticmethod
    def train_test_for_iteration(model, c1, c2, testing_data, epoch, batch_size, iterations,
                                 accuracy_thresh_hold):
        """Train the model for n epochs and then check it with 0.3 of the data (validation), the model accuracy
        is checked if it achieve the wanted accuracy test will run and saved in M.\n
        The data for testing the anchor is divided that they contain in the first place
        the anchor and the rest are for Testing."""
        results = []
        M = []
        data_names = ['accuracy', 'val_accuracy', 'loss', 'val_loss']
        result = DataFrame()

        while iterations > 0:
            x_train, y_train = DM.DataManagement.create_new_batch(c1, c2)

            # for the CNN
            x_train = np.reshape(x_train, np.append(x_train.shape, 1))

            history = model.fit(x_train, y_train, validation_split=.30, epochs=epoch, batch_size=batch_size, verbose=1)

            if history.history['accuracy'][-1] >= accuracy_thresh_hold:
                # test the model if the wanted accuracy is achieved
                iterations -= 1

                M.append(Bi_Direct_LSTM.test_model(model, testing_data.anchor_c1, testing_data.anchor_c2,
                                                   testing_data.c1_test, testing_data.c2_test, testing_data.c3_test))

                temp = DataFrame()
                for data_name in data_names:
                    temp[data_name] = history.history[data_name]
                result = result.append(temp, ignore_index=True)

            # model.reset_states()

        # plot the result
        result.plot()
        plt.show(block=False)

        return history, M, model

    @staticmethod
    def test_model(model, anchor_c1, anchor_c2, c1, c2, c3):
        """Test the model by running anchor dataSet(c1, c2) and additional
        data(c1, c2, c3). return numpy array concatenate of all the classes results
        the order of the data is anchors(c1, c2), c1,c2,c3"""

        c1_anchor_prediction = Bi_Direct_LSTM.make_prediction(model, anchor_c1)
        c2_anchor_prediction = Bi_Direct_LSTM.make_prediction(model, anchor_c2)
        c3_prediction = Bi_Direct_LSTM.make_prediction(model, c3)
        c1_prediction = Bi_Direct_LSTM.make_prediction(model, c1)
        c2_prediction = Bi_Direct_LSTM.make_prediction(model, c2)

        prediction_t = np.concatenate((c1_anchor_prediction, c2_anchor_prediction), axis=0)
        prediction_t = np.concatenate((prediction_t, c1_prediction), axis=0)
        prediction_t = np.concatenate((prediction_t, c2_prediction), axis=0)

        return np.concatenate((prediction_t, c3_prediction), axis=0)

    @staticmethod
    def make_prediction(model, data_list):
        """The method receive a list of books data and run on each book and get the mean values
        for all the predictions, it return the result as numpy array"""
        predictions_list = []
        for data in data_list:
            prediction_res = np.zeros(shape=(2,))

            # for the CNN
            # add chanel dim
            data = np.reshape(data, np.append(data.shape, 1))

            predictions = model.predict(data)
            for prediction in predictions:
                prediction_res = np.add(prediction_res, prediction)

            predictions_list.append(prediction_res / len(data))

        return np.array(predictions_list, dtype='f')
