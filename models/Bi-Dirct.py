import numpy as np
import traceback

import models.LSTM.Bi_Direct_LSTM as BD_lstm
import models.LoadingBalancingData.DataManagement as DM
import models.K_means_Siluete.K_means_Siluete as KMS
import models.LSTM.Save_results as SR

# to run on the GPU and solve a bug
# gpu_devices = tf.config.experimental.list_physical_devices('GPU')
# for device in gpu_devices:
#     tf.config.experimental.set_memory_growth(device, True)


# parameters
embedding_size = 300
tweet_length = 200
bi_lstm_hidden_state_size = 50
drop_out = 0.4
learning_rate = 0.001
epoch = 15
batch_size = 100
iterations = 2
fully_connected_layer = 30

lstm = BD_lstm.Bi_Direct_LSTM(bi_lstm_hidden_state_size=bi_lstm_hidden_state_size,
                              tweet_length=tweet_length,
                              embedding_size=embedding_size,
                              drop_out=drop_out,
                              fully_connected_layer=fully_connected_layer,
                              learning_rate=learning_rate,
                              loss_func='binary_crossentropy')

c1, c2, c3, anchor_c1, anchor_c2 = DM.DataManagement.load_data(tweet_length, embedding_size, 7, 2)

history, M = BD_lstm.Bi_Direct_LSTM.train_test_for_iteration(model=lstm.model, c1=c1, c2=c2,
                                                             anchor_c1=anchor_c1, anchor_c2=anchor_c2,
                                                             c3=c3, epoch=epoch, batch_size=batch_size,
                                                             iterations=iterations, accuracy_thresh_hold=0.75)

M = np.concatenate(M, axis=0)

iteration_size = 1 + 1 + len(anchor_c1) - 1 + len(anchor_c2) - 1 + len(c3)
BD_lstm.Bi_Direct_LSTM.show_results_of_tests(M=M, len_anchor_c1=1, len_anchor_c2=1, len_c1=len(anchor_c1) - 1,
                                             len_c2=len(anchor_c2) - 1, len_c3=len(c3))

try:
    labels, kmeans = KMS.calculate_plot_Kmeans(M, iteration_size)
    score = KMS.silhouette(M=M, labels=labels, kmeans=kmeans, iteration_size=iteration_size)
    SR.save_history_data(tweet_length, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                         history, learning_rate, embedding_size, score)
except Exception as e:
    print(str(e)+'\n'+traceback.format_exc())
