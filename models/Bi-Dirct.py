import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer
import matplotlib.pyplot as plt

import models.LSTM.Bi_Direct_LSTM as BD_lstm
import models.LoadingBalancingData.DataManagement as DM

# to run on the GPU and solve a bug
# gpu_devices = tf.config.experimental.list_physical_devices('GPU')
# for device in gpu_devices:
#     tf.config.experimental.set_memory_growth(device, True)


# parameters
embedding_size = 100
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

BD_lstm.Bi_Direct_LSTM.show_results_of_tests(M=M, len_anchor_c1=1, len_anchor_c2=1, len_c1=len(anchor_c1)-1,
                                             len_c2=len(anchor_c2)-1, len_c3= len(c3))

# the K-means
M = np.concatenate(M, axis=0)

kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=100, random_state=42)
labels = kmeans.fit_predict(M)

plt.scatter(M[:, 0], M[:, 1], c=labels, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.3)
plt.show()

score = silhouette_score(M, labels=labels, metric='euclidean')
print("The Silhouette score is :" + str(score))

visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')
visualizer.fit(M)
visualizer.show()


def save_history_data():
    # file for saving the result and the parameters
    file = open("result_checks.txt", "a")

    file.write("-- tweet len:{0}, epochs:{1}, batch_size={2}, drop_out={3}, bi_lstm_hidden_state_size:{4}"
               "\naccuracy:{5}, validation accuracy: {6}, learning rate: {7}, embedding_size: {8}\n"
               "The Silhouette score: {9}\n".format(
        tweet_length, epoch, batch_size, drop_out,
        bi_lstm_hidden_state_size, sum(history.history['accuracy']) / len(history.history['accuracy']),
                                   sum(history.history['val_accuracy']) / len(history.history['val_accuracy']),
        learning_rate,
        embedding_size, score))
    file.close()
