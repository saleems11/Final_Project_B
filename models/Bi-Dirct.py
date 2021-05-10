import numpy as np
import traceback
import matplotlib.pyplot as plt
from time import sleep

import models.LSTM.Bi_Direct_LSTM as BD_lstm
import models.LoadingBalancingData.DataManagement as DM
import models.K_means_Siluete.K_means_Siluete as KMS
import models.LSTM.Save_results as SR

from Show_results import Heat_map, Book_chunks_labels, Error_bar, Histograms
from Exceptions.Exceptions import SilhouetteBellowThreshold, AnchorsInSameCluster
import keras.losses as losses
import Tests.send_mail as SM
from Objects.SmartChecking import SmartChecking
from utils.doc_utils import Documents_utils

""" To make the code better embed each book and save it"""

change_your_mail_address = False
receiver = "iamme0ssa@gmail.com"
if change_your_mail_address:
    print("Hello my freind, please change the email address, so the messages will be"
          "sent to you, have a nice day")
    exit()

# parameters
embedding_size = 1024
tweet_size = 200
bi_lstm_hidden_state_size = 160
drop_out = 0.3
learning_rate = 0.001
epoch = 10
batch_size = 100
iterations = 10
fully_connected_layer = 30
silhouette_threshold = 0.45
accuracy_thresh_hold = 0.96
loss_func = 'binary_crossentropy'
# losses.
# binary_crossentropy, categorical_crossentropy
load_saved_model = False
model_name = "book_classification_dim_{0}_sil_{1}".format(300, 0.83)

c1_anchor_name = ["Al_Mankhul_min_Taliqat_al_Usul"]
c2_anchor_name = ["Kimiya_yi_Saadat"]
c1_test_names = ["Al_Mustasfa_min_ilm_al_Usul", "Fada_ih_al_Batiniyya_wa_Fada_il_al_Mustazhiriyy",
                 "Faysal_at_Tafriqa_Bayna_al_Islam_wa_al_Zandaqa", "al_iqtisad_fi_al_itiqad",
                 "Iljam_Al_Awamm_an_Ilm_Al_Kalam", "Tahafut_al_Falasifa"]
c2_test_names = ["al_Madnun_bihi_ala_ghayri"]
c3_test_names = ["Mishakat_al_Anwar"]

finished = False
prev_tweet_length = -1

smartChecking = SmartChecking()

while not finished:

    # parameters = smartChecking.new_parameters_values()
    # tweet_size = parameters[0]
    # bi_lstm_hidden_state_size = parameters[1]
    # learning_rate = parameters[2]
    # fully_connected_layer = parameters[3]
    # batch_size = parameters[4]
    # epoch = parameters[5]
    # drop_out = parameters[6]

    score = 0
    if prev_tweet_length == -1 or prev_tweet_length == tweet_size:
        c1, c2, testing_data = DM.DataManagement.load_data(tweet_size=tweet_size, embedding_size=embedding_size,
                                                           c1_anchor_name=c1_anchor_name, c2_anchor_name=c2_anchor_name,
                                                           c1_test_names=c1_test_names, c2_test_names=c2_test_names,
                                                           c3_test_names=c3_test_names, c1_dir=Documents_utils.c1, c2_dir=Documents_utils.c2,
                                                           c3_dir=Documents_utils.c3)

    # save the prev tweet size
    prev_tweet_length = tweet_size

    lstm = BD_lstm.Bi_Direct_LSTM(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                                  tweet_length=tweet_size,
                                  embedding_size=embedding_size,
                                  drop_out=drop_out,
                                  fully_connected_layer=fully_connected_layer,
                                  learning_rate=learning_rate,
                                  loss_func=loss_func)

    history, M = BD_lstm.Bi_Direct_LSTM.train_test_for_iteration(model=lstm.model, c1=c1, c2=c2,
                                                                 testing_data=testing_data, epoch=epoch,
                                                                 batch_size=batch_size, iterations=iterations,
                                                                 accuracy_thresh_hold=accuracy_thresh_hold,
                                                                 f1=3, f2=2)

    # lstm.model = model
    if len(M) == 0:
        print("M len is zero")
    M = np.concatenate(M, axis=0)
    testing_data.show_results_of_tests(M=M, labels=[])

    try:
        labels, kmeans = KMS.calculate_plot_Kmeans(M, testing_data.iteration_size, testing_data)
        testing_data.show_results_of_tests(M=M, labels=labels)

        score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans,
                               iteration_size=testing_data.iteration_size, silhouette_threshold=silhouette_threshold)

        SR.save_history_data(tweet_size, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                             history, learning_rate, embedding_size, score, iterations, fully_connected_layer)
        finished = True

        # # show the heat map
        # Heat_map.create_heat_map(Heat_map.convert_M_to_heat_map(M=M, iteration_size=testing_data.iteration_size))
        #
        # # show Error_bar
        # # Error_bar.create_error_bar(["hello", "how", "hi"], [10, 12, 13], 11, 12, 10, "Testing", [[1, 2, 3], [3, 1, 1]])
        # books_names, books_mean_values_over_all_iter, books_error_down_values_over_all_iter, \
        # books_error_up_values_over_all_iter, books_mean_values_over_all_iter, c1_mean_val, c2_mean_val, mean_val\
        #     = testing_data.get_error_bar_data()
        #
        # Error_bar.Error_bar.create_error_bar(x=books_names,
        #                                      y=books_mean_values_over_all_iter,
        #                                      y_mean=mean_val,
        #                                      y_mean_c1=c1_mean_val,
        #                                      y_mean_c2=c2_mean_val,
        #                                      label="Books Error Bar",
        #                                      asymmetric_y_error=[books_error_down_values_over_all_iter,
        #                                                          books_error_up_values_over_all_iter])

        # save the model
        # lstm.model.save("book_classification_dim_%d_sil_%.2f_%d_itter" % (embedding_size, score, iterations))


    except SilhouetteBellowThreshold as e:
        # SM.send_mail(receiver, "Al-Ghazali project", str(e))
        score = e.silhouette_val
        print(str(e) + '\n' + traceback.format_exc())
    except AnchorsInSameCluster as e:
        # SM.send_mail(receiver, "Al-Ghazali project", str(e))
        print(str(e) + '\n' + traceback.format_exc())
    finally:
        # show the heat map
        Heat_map.Heat_map.create_heat_map(
            Heat_map.Heat_map.convert_M_to_heat_map(M=M, iteration_size=testing_data.iteration_size))

        books_names, books_mean_values_over_all_iter, books_error_down_values_over_all_iter, \
        books_error_up_values_over_all_iter, books_mean_values_over_all_iter, c1_mean_val, c2_mean_val, mean_val \
            = testing_data.get_error_bar_data()

        Error_bar.Error_bar.create_error_bar(x=books_names,
                                             y=books_mean_values_over_all_iter,
                                             y_mean=mean_val,
                                             y_mean_c1=c1_mean_val,
                                             y_mean_c2=c2_mean_val,
                                             label="Books Error Bar",
                                             asymmetric_y_error=[books_error_down_values_over_all_iter,
                                                                 books_error_up_values_over_all_iter])

        testing_data.set_book_mean_prediction_val_over_iter(testing_data.books[0])

        # book_chunks labels
        Book_chunks_labels.Book_chunks_labels.create_book_over_iterations_chunks_labels(
            testing_data.books[0].mean_of_mean_prediction_res_over_iter,
            testing_data.books[0].book_name + ' prediction')

        rounded_array = Book_chunks_labels.Book_chunks_labels.round_to_three_values(
            testing_data.books[0].mean_of_mean_prediction_res_over_iter, 0,
            0.5, 1)

        Book_chunks_labels.Book_chunks_labels.create_book_over_iterations_chunks_labels(
            rounded_array, testing_data.books[0].book_name + ' labels')

        # hitogram
        Histograms.Histograms.create_Histograms(testing_data.books[0].mean_of_mean_prediction_res_over_iter,
                                                testing_data.books[0].book_name)

        # plt.close('all')
        sleep(10)
        print("Running Again")

    SR.save_history_data(tweet_size, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                         history, learning_rate, embedding_size, score, iterations, fully_connected_layer)

SM.send_mail(receiver, "Al-Ghazali project", "Saleem it had finished calculation")
