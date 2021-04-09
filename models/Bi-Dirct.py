import numpy as np
import traceback
import matplotlib.pyplot as plt
from time import sleep

import models.LSTM.Bi_Direct_LSTM as BD_lstm
import models.LoadingBalancingData.DataManagement as DM
import models.K_means_Siluete.K_means_Siluete as KMS
import models.LSTM.Save_results as SR

import Tests.send_mail as SM


change_your_mail_address = False
receiver = "iamme0ssa@gmail.com"
if change_your_mail_address:
    print("Hello my freind, please change the email address, so the messages will be"
          "sent to you, have a nice day")
    exit()


# parameters
embedding_size = 1024
tweet_length = 200
bi_lstm_hidden_state_size = 50
drop_out = 0.4
learning_rate = 0.001
epoch = 15
batch_size = 100
iterations = 1
fully_connected_layer = 30
silhouette_threshold = 0.8
accuracy_thresh_hold = 0.75
loss_func = 'binary_crossentropy'
load_saved_model = False
model_name = "book_classification_dim_{0}_sil_{1}".format(300, 0.83)

finished = False
first_time = True

while not finished:
    lstm = BD_lstm.Bi_Direct_LSTM(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                                  tweet_length=tweet_length,
                                  embedding_size=embedding_size,
                                  drop_out=drop_out,
                                  fully_connected_layer=fully_connected_layer,
                                  learning_rate=learning_rate,
                                  loss_func=loss_func)
    if first_time:
        c1, c2, c3, anchor_c1, anchor_c2 = DM.DataManagement.load_data(tweet_length, embedding_size, 7, 2)
        first_time = False

    history, M, model = BD_lstm.Bi_Direct_LSTM.train_test_for_iteration(model=lstm.model, c1=c1, c2=c2,
                                                                 anchor_c1=anchor_c1, anchor_c2=anchor_c2,
                                                                 c3=c3, epoch=epoch, batch_size=batch_size,
                                                                 iterations=iterations,
                                                                 accuracy_thresh_hold=accuracy_thresh_hold)

    lstm.model = model
    M = np.concatenate(M, axis=0)

    iteration_size = 1 + 1 + len(anchor_c1) - 1 + len(anchor_c2) - 1 + len(c3)
    BD_lstm.Bi_Direct_LSTM.show_results_of_tests(M=M, len_anchor_c1=1, len_anchor_c2=1, len_c1=len(anchor_c1) - 1,
                                                 len_c2=len(anchor_c2) - 1, len_c3=len(c3))

    try:
        labels, kmeans = KMS.calculate_plot_Kmeans(M, iteration_size)
        score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans,
                               iteration_size=iteration_size, silhouette_threshold=silhouette_threshold)

        # save the model
        lstm.model.save("book_classification_dim_{0}_sil_{1}".format(embedding_size, score))

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