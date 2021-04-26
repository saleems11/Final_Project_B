import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv1D
from keras.layers import Dense, MaxPooling1D, Flatten

class Conv_1D:

    def __init__(self):
        self.model = None
        pass

    @staticmethod
    def create_1D_conv_words_model(embedding_size, filters=10, kernel_size=7, activation_1='relu'):
        """ input shape = [None, 1024]"""

        # define model
        model = Sequential()

        model.add(Conv1D(filters=filters,
                         kernel_size=kernel_size,
                         activation=activation_1,
                         input_shape=(None, embedding_size)))
        model.add(MaxPooling1D(pool_size=2))

        model.add(Conv1D(filters=filters,
                         kernel_size=kernel_size,
                         activation=activation_1))
        model.add(MaxPooling1D(pool_size=2))

        model.add(Flatten())
        model.add(Dense(10, activation=activation_1))
        model.add(Dense(1, activation='sigmoid'))

        print(model.summary())
        opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(loss=loss_func, optimizer=opt, metrics=['accuracy'])
