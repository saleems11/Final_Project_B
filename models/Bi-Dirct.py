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

""" To make the code better embed each book and save it"""

change_your_mail_address = False
receiver = "iamme0ssa@gmail.com"
if change_your_mail_address:
    print("Hello my freind, please change the email address, so the messages will be"
          "sent to you, have a nice day")
    exit()

# parameters
embedding_size = 1024
tweet_size = 300
bi_lstm_hidden_state_size = 192
drop_out = 0.35
learning_rate = 0.01
epoch = 10
batch_size = 100
iterations = 2
fully_connected_layer = 30
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
first_time = True


class SmartChecking:
    tweet_size_options = [200, 300, 400]
    bi_lstm_hidden_state_size_min = 32
    bi_lstm_hidden_state_size_max = 256
    bi_lstm_hidden_state_size_jump = 32
    learning_rate_max = 0.01
    learning_rate_min = 0.001
    learning_rate_jump = 0.001
    fully_connected_layer_min = 20
    fully_connected_layer_max = 60
    fully_connected_layer_jump = 10
    batch_size_min = 64
    batch_size_max = 320
    batch_size_jump = 64
    epoch_min = 10
    epoch_max = 25
    epoch_jump = 5
    drop_out_min = 0.1
    drop_out_max = 0.6
    drop_out_jump = 0.1
    """
    0 tweet_size_options
    1 bi_lstm_hidden_state_size
    2 learning_rate
    3 fully_connected_layer
    4 batch_size
    5 epoch
    6 drop_out"""
    parameter_idx = 0
    num_of_param = 7
    options_state = [2, 2, 2, 2, 1, 1, 1]
    parameters_options = [0] * 7

    @staticmethod
    def set_parameters_options_number():
        SmartChecking.parameters_options[0] = len(SmartChecking.tweet_size_options)
        SmartChecking.parameters_options[1] = int((SmartChecking.bi_lstm_hidden_state_size_max -
                                                   SmartChecking.bi_lstm_hidden_state_size_min) /
                                                  SmartChecking.bi_lstm_hidden_state_size_jump) + 1

        SmartChecking.parameters_options[2] = int((SmartChecking.learning_rate_max -
                                                   SmartChecking.learning_rate_min) /
                                                  SmartChecking.learning_rate_jump) + 1

        SmartChecking.parameters_options[3] = int((SmartChecking.fully_connected_layer_max -
                                                   SmartChecking.fully_connected_layer_min) /
                                                  SmartChecking.fully_connected_layer_jump) + 1

        SmartChecking.parameters_options[4] = int((SmartChecking.batch_size_max -
                                                   SmartChecking.batch_size_min) /
                                                  SmartChecking.batch_size_jump) + 1

        SmartChecking.parameters_options[5] = int((SmartChecking.epoch_max -
                                                   SmartChecking.epoch_min) /
                                                  SmartChecking.epoch_jump) + 1

        SmartChecking.parameters_options[6] = int((SmartChecking.drop_out_max -
                                                   SmartChecking.drop_out_min) /
                                                  SmartChecking.drop_out_jump) + 1

    @staticmethod
    def new_parameters_values():
        print(SmartChecking.options_state)

        res = [SmartChecking.tweet_size_options[SmartChecking.options_state[0]],

                SmartChecking.bi_lstm_hidden_state_size_min +
                (SmartChecking.bi_lstm_hidden_state_size_jump *
                 SmartChecking.options_state[1]),

                SmartChecking.learning_rate_min +
                (SmartChecking.learning_rate_jump *
                 SmartChecking.options_state[2]),

                SmartChecking.fully_connected_layer_min +
                (SmartChecking.fully_connected_layer_jump *
                 SmartChecking.options_state[3]),

                SmartChecking.batch_size_min +
                (SmartChecking.batch_size_jump *
                 SmartChecking.options_state[4]),

                SmartChecking.epoch_min +
                (SmartChecking.epoch_jump *
                 SmartChecking.options_state[5]),

                SmartChecking.drop_out_min +
                (SmartChecking.drop_out_jump *
                 SmartChecking.options_state[6])
                ]

        SmartChecking.options_state[SmartChecking.parameter_idx] = \
            (SmartChecking.options_state[SmartChecking.parameter_idx] + 1) % \
            SmartChecking.parameters_options[SmartChecking.parameter_idx]

        SmartChecking.parameter_idx = (SmartChecking.parameter_idx + 1) % SmartChecking.num_of_param

        print(res)
        return res


SmartChecking.set_parameters_options_number()


while not finished:
    parameters = SmartChecking.new_parameters_values()
    tweet_size_options = parameters[0]
    bi_lstm_hidden_state_size = parameters[1]
    learning_rate = parameters[2]
    fully_connected_layer = parameters[3]
    batch_size = parameters[4]
    epoch = parameters[5]
    drop_out = parameters[6]

    if first_time:
        c1, c2, testing_data = DM.DataManagement.load_data(tweet_size=tweet_size, embedding_size=embedding_size,
                                                           c1_anchor_name=c1_anchor_name, c2_anchor_name=c2_anchor_name,
                                                           c1_test_names=c1_test_names, c2_test_names=c2_test_names,
                                                           c3_test_names=c3_test_names)
        first_time = False

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
        SM.send_mail(receiver, "Al-Ghazali project", str(e))
        score = e.silhouette_val
        print(str(e) + '\n' + traceback.format_exc())
    except AnchorsInSameCluster as e:
        SM.send_mail(receiver, "Al-Ghazali project", str(e))
        print(str(e) + '\n' + traceback.format_exc())
    finally:
        plt.close('all')
        sleep(10)
        print("Running Again")

    SR.save_history_data(tweet_size, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                         history, learning_rate, embedding_size, score)


SM.send_mail(receiver, "Al-Ghazali project", "Saleem it had finished calculation")
