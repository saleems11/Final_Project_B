import numpy as np
import traceback
import matplotlib.pyplot as plt
from time import sleep

import models.LSTM.Bi_Direct_LSTM as BD_lstm
import models.LoadingBalancingData.DataManagement as DM
import models.K_means_Siluete.K_means_Siluete as KMS
import models.LSTM.Save_results as SR

import Tests.send_mail as SM
import Objects.TestingData as TD

""" To make the code better embed each book and save it"""

change_your_mail_address = True
receiver = "iamme0ssa@gmail.com"
if change_your_mail_address:
    print("Hello my freind, please change the email address, so the messages will be"
          "sent to you, have a nice day")
    exit()


# parameters
embedding_size = 300
tweet_length = 200
bi_lstm_hidden_state_size = 50
drop_out = 0.4
learning_rate = 0.001
epoch = 15
batch_size = 100
iterations = 6
fully_connected_layer = 30
silhouette_threshold = 0.85
accuracy_thresh_hold = 0.75
loss_func = 'binary_crossentropy'
load_saved_model = False
model_name = "book_classification_dim_{0}_sil_{1}".format(300, 0.83)

finished = False
first_time = True

while not finished:

    if first_time:
        c1, c2, c3, test_c1, test_c2 = DM.DataManagement.load_data(tweet_length, embedding_size, 7, 2)
        testing_data = TD.TestingData(test_c1, test_c2, c3)
        first_time = False

    lstm = BD_lstm.Bi_Direct_LSTM(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                                  tweet_length=tweet_length,
                                  embedding_size=embedding_size,
                                  drop_out=drop_out,
                                  fully_connected_layer=fully_connected_layer,
                                  learning_rate=learning_rate,
                                  loss_func=loss_func)

    history, M, model = BD_lstm.Bi_Direct_LSTM.train_test_for_iteration(model=lstm.model, c1=c1, c2=c2,
                                                                        test_c1=test_c1, test_c2=test_c2,
                                                                        c3=c3, epoch=epoch, batch_size=batch_size,
                                                                        iterations=iterations,
                                                                        accuracy_thresh_hold=accuracy_thresh_hold)

    lstm.model = model
    M = np.concatenate(M, axis=0)

    testing_data.show_results_of_tests(M=M)

    try:
        labels, kmeans = KMS.calculate_plot_Kmeans(M, testing_data.iteration_size)
        score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans,
                               iteration_size=testing_data.iteration_size, silhouette_threshold=silhouette_threshold)

        # save the model
        lstm.model.save("book_classification_dim_%d_sil_%.2f" % (embedding_size, score))

        SR.save_history_data(tweet_length, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                             history, learning_rate, embedding_size, score)
        finished = True



    except Exception as e:
        SM.send_mail(receiver, "Al-Ghazali project", str(e))
        plt.close('all')
        sleep(10)
        print("Running Again")
        print(str(e) + '\n' + traceback.format_exc())

SM.send_mail(receiver, "Al-Ghazali project","Saleem it had finished calculation")