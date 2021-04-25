import numpy as np
import traceback
import matplotlib.pyplot as plt
from time import sleep

import models.LSTM.Bi_Direct_LSTM as BD_lstm
import models.LoadingBalancingData.DataManagement as DM
import models.K_means_Siluete.K_means_Siluete as KMS
import models.LSTM.Save_results as SR
from Exceptions.Exceptions import SilhouetteBellowThreshold, AnchorsInSameCluster
import keras.losses as losses
import Tests.send_mail as SM
from Objects.SmartChecking import SmartChecking

""" To make the code better embed each book and save it"""

change_your_mail_address = False
receiver = "iamme0ssa@gmail.com"
if change_your_mail_address:
    print("Hello my freind, please change the email address, so the messages will be"
          "sent to you, have a nice day")
    exit()

# parameters
embedding_size = 300
tweet_size = 200
bi_lstm_hidden_state_size = 160
drop_out = 0.4
learning_rate = 0.004
epoch = 10
batch_size = 128
iterations = 10
fully_connected_layer = 45
silhouette_threshold = 0.75
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
                                                           c3_test_names=c3_test_names)

    # save the prev tweet size
    prev_tweet_length = tweet_size


    lstm = BD_lstm.Bi_Direct_LSTM(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                                  tweet_length=tweet_size,
                                  embedding_size=embedding_size,
                                  drop_out=drop_out,
                                  fully_connected_layer=fully_connected_layer,
                                  learning_rate=learning_rate,
                                  loss_func=loss_func)

    history, M, model = BD_lstm.Bi_Direct_LSTM.train_test_for_iteration(model=lstm.model, c1=c1, c2=c2,
                                                                        testing_data=testing_data, epoch=epoch,
                                                                        batch_size=batch_size, iterations=iterations,
                                                                        accuracy_thresh_hold=accuracy_thresh_hold)

    lstm.model = model
    if len(M) == 0:
        print("M len is zero")
    M = np.concatenate(M, axis=0)
    testing_data.show_results_of_tests(M=M, labels=[])

    try:
        labels, kmeans = KMS.calculate_plot_Kmeans(M, testing_data.iteration_size, testing_data)
        testing_data.show_results_of_tests(M=M, labels=labels)

        score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans,
                               iteration_size=testing_data.iteration_size, silhouette_threshold=silhouette_threshold)

        # save the model
        lstm.model.save("book_classification_dim_%d_sil_%.2f_%d_itter" % (embedding_size, score, iterations))

        SR.save_history_data(tweet_size, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                             history, learning_rate, embedding_size, score)
        finished = True



    except SilhouetteBellowThreshold as e:
        # SM.send_mail(receiver, "Al-Ghazali project", str(e))
        score = e.silhouette_val
        print(str(e) + '\n' + traceback.format_exc())
    except AnchorsInSameCluster as e:
        # SM.send_mail(receiver, "Al-Ghazali project", str(e))
        print(str(e) + '\n' + traceback.format_exc())
    finally:
        plt.close('all')
        sleep(10)
        print("Running Again")

    SR.save_history_data(tweet_size, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                         history, learning_rate, embedding_size, score, iterations, fully_connected_layer)


SM.send_mail(receiver, "Al-Ghazali project", "Saleem it had finished calculation")
