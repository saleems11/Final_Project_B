import tensorflow as tf
import models.K_means_Siluete.K_means_Siluete as KMS

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Bidirectional

from pandas import DataFrame
import numpy as np
from time import time

import models.LoadingBalancingData.DataManagement as DM
from GUI.App.pages.process_bar import ProcessBar
from .Parameters import Parameters
from Objects.TestingData import TestingData

class Bi_Direct_LSTM:
    """ A Class for creating Bi-Direct lstm and training, testing it"""

    def __init__(self, parameters: Parameters, process_bar: ProcessBar,  estimated_time_remaining: [float]):
        """ create the model and set his parameter, and set the ProcessBar, and estimated_time_remaining """
        # to run on the GPU and solve a bug
        gpu_devices = tf.config.experimental.list_physical_devices('GPU')
        for device in gpu_devices:
            tf.config.experimental.set_memory_growth(device, True)
        self.parameters = parameters
        # creating the model
        self.model = self.create_model()
        self.process_bar: ProcessBar = process_bar
        self.history = None

        # for remaining time estimation
        self.prev_iteration = 0
        self.last_iter_starting_time = None
        self.estimated_time_remaining = estimated_time_remaining
        self.average_iteration_time = 0
        self.total_time = 0


    def create_model(self):
        """Create a Bi-Direct LSTM model that is specified according to the parameters, and return the model.
        The model have 5 layers(Bi-direct(LSTM)[the result are concat], DropOut, fully connected layer, DropOut,
        softMax).\n
        (for the LSTM model there is a need to reset the hidden and cell state after
        each epoch and that is done when creating the model with the parameter stateful=False)"""
        model = Sequential()
        model.add(Bidirectional(
            LSTM(units=self.parameters.lstm_hidden_state_size, return_sequences=False, stateful=False),
            input_shape=(self.parameters.tweet_length, 1024),
            merge_mode="concat"))

        model.add(Dropout(self.parameters.drop_out))
        if self.parameters.activation_function == 'RElu':
            model.add(Dense(self.parameters.fully_connect_layer, activation='relu'))
        elif self.parameters.activation_function == "Sigmoid":
            model.add(Dense(self.parameters.fully_connect_layer, activation='sigmoid'))

        model.add(Dropout(self.parameters.drop_out))
        model.add(Dense(2, activation='softmax'))

        print(model.summary())
        # set the optimizer
        if self.parameters.optimizer == 'Adam':
            opt = tf.keras.optimizers.Adam(learning_rate=self.parameters.learning_rate)
        elif self.parameters.optimizer == 'SGD':
            opt = tf.keras.optimizers.SGD(learning_rate=self.parameters.learning_rate)
        elif self.parameters.optimizer == 'Adagrad':
            opt = tf.keras.optimizers.Adagrad(learning_rate=self.parameters.learning_rate)
        elif self.parameters.optimizer == 'AdaDelta':
            opt = tf.keras.optimizers.Adadelta(learning_rate=self.parameters.learning_rate)
        else:
            opt = tf.keras.optimizers.RMSprop(learning_rate=self.parameters.learning_rate)
        #     set the loss functions
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

        return model

    def train_test_for_iteration(self, c1, c2, testing_data:TestingData):
        """Train the model for n epochs and then check it with 0.2 of the data (validation), the model accuracy
        is checked if it achieve the wanted accuracy test will run and saved in M.
        The data for testing the anchor is divided that they contain in the first place
        the anchor and the rest are for Testing.
        :parameters
        c1: training data for real data
        c2: training data for fake data
        :returns
        self.history: the accuracy and the loss over iteration and epoch results
        M: mean prediction result of each iteration of each book
        score: the silhouette score of M
        book_names_in_order: book names as the same order
        """
        results = []
        M = []
        data_names = ['accuracy', 'val_accuracy', 'loss', 'val_loss']
        book_names_in_order = None
        result = DataFrame()
        iterations = self.parameters.number_of_iteration
        self.last_iter_starting_time = time()

        while iterations > 0:
            # update the progress bar
            self.set_iteration(self.parameters.number_of_iteration - iterations, iterations)

            # create new batch
            x_train, y_train = DM.DataManagement.create_new_batch(c1, c2, self.parameters.multiplying_rate, self.parameters.undersampling_rate)
            # train the model
            self.history = self.model.fit(x_train, y_train, validation_split=.20, epochs=self.parameters.number_of_epoch,
                                batch_size=self.parameters.batch_size, verbose=1)

            if self.history.history['accuracy'][-1] >= self.parameters.accuracy_threshold:
                # test the model if the wanted accuracy is achieved

                # for time estimating
                iterations -= 1
                self.prev_iteration = self.prev_iteration + 1
                self.total_time += time() - self.last_iter_starting_time
                self.last_iter_starting_time = time()
                self.average_iteration_time = self.total_time/self.prev_iteration
                self.estimated_time_remaining[0] = self.average_iteration_time * iterations

                print("Remaining iterations to run %d"%iterations)

                """ start of changed code """
                # test the model
                # books_prediction_results, book_names_in_order = Bi_Direct_LSTM.test_model(self.model, testing_data.anchor_c1, testing_data.anchor_c2,
                #                           testing_data.c1_test, testing_data.c2_test, testing_data.c3_test)
                books_prediction_results = Bi_Direct_LSTM.make_prediction(self.model, testing_data.books)
                """ End of changed code """
                M.append(books_prediction_results)

                temp = DataFrame()
                for data_name in data_names:
                    temp[data_name] = self.history.history[data_name]
                result = result.append(temp, ignore_index=True)


            # self.model.reset_states()
        if M:
            self.set_iteration(self.parameters.number_of_iteration - iterations + 1, iterations)

            M = np.concatenate(M, axis=0)
            # calculate k-means
            labels, kmeans = KMS.calculate_plot_Kmeans(M, testing_data.iteration_size, testing_data)
            # calculate silhouette
            score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans,
                                   iteration_size=testing_data.iteration_size,
                                   silhouette_threshold=self.parameters.silhouette_threshold)
        else:
            score = 0
        """ start of changed code """
        # return self.history, M, score, book_names_in_order
        return self.history, M, score
        """ start of changed code """

    def set_iteration(self, current_iteration:int, iterations:int):
        """ set the process bar data , the iteration status label, and progress bar value """
        self.process_bar.status = f'{(self.parameters.number_of_iteration - iterations)} / {self.parameters.number_of_iteration}'
        self.process_bar.process = current_iteration/self.parameters.number_of_iteration

    # @staticmethod
    # def test_model(model, anchor_c1, anchor_c2, c1, c2, c3):
    #     """Test the model by running anchor dataSet(c1, c2) and additional
    #     test data(c1, c2, unknown(c3)). return numpy array concatenate of all the classes results
    #     the order of the data is anchors(c1, c2), c1, c2, c3"""
    #     books_names_as_M = []
    #     c1_anchor_prediction = Bi_Direct_LSTM.make_prediction(model, anchor_c1)
    #     c2_anchor_prediction = Bi_Direct_LSTM.make_prediction(model, anchor_c2)
    #     c3_prediction = Bi_Direct_LSTM.make_prediction(model, c3)
    #     c1_prediction = Bi_Direct_LSTM.make_prediction(model, c1)
    #     c2_prediction = Bi_Direct_LSTM.make_prediction(model, c2)
    #
    #     prediction_t = np.concatenate((c1_anchor_prediction, c2_anchor_prediction), axis=0)
    #     for book in anchor_c1:
    #         books_names_as_M.append(book.book_name)
    #     for book in anchor_c2:
    #         books_names_as_M.append(book.book_name)
    #
    #     prediction_t = np.concatenate((prediction_t, c1_prediction), axis=0)
    #     for book in c1:
    #         books_names_as_M.append(book.book_name)
    #
    #     prediction_t = np.concatenate((prediction_t, c2_prediction), axis=0)
    #     for book in c2:
    #         books_names_as_M.append(book.book_name)
    #
    #     for book in c3:
    #         books_names_as_M.append(book.book_name)
    #     return np.concatenate((prediction_t, c3_prediction), axis=0), books_names_as_M


    def test_model(self, testing_data:TestingData):
        M = []
        """ make the prediction """
        books_prediction_results = Bi_Direct_LSTM.make_prediction(self.model, testing_data.books)
        M.append(books_prediction_results)

        if M:
            # self.set_iteration(1, 1)

            M = np.concatenate(M, axis=0)
            # calculate k-means
            labels, kmeans = KMS.calculate_plot_Kmeans(M, testing_data.iteration_size, testing_data)
            # calculate silhouette
            score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans,
                                   iteration_size=testing_data.iteration_size,
                                   silhouette_threshold=self.parameters.silhouette_threshold)
        else:
            score = 0
        return M, score

    @staticmethod
    def make_prediction(model, books_list):
        """The method receive a list of book object and run on each book and get the mean values
        for all the predictions, it return the result as numpy array"""
        predictions_list = []
        for idx in range(len(books_list)):
            #  calculate prediction for each book
            prediction_res = 0
            predictions = model.predict(books_list[idx].embedded_data)
            for prediction in predictions:
                prediction_res += prediction[0]

            # mean prediction results
            mean_predictions = prediction_res / len(books_list[idx].embedded_data)
            # save the prediction result to the testing data
            books_list[idx].add_prediction_res(predictions=predictions[:, 0], mean_predictions=mean_predictions)
            predictions_list.append(mean_predictions)

        # dtype='f' for smaller memory usage
        return np.array(predictions_list, dtype='f')


