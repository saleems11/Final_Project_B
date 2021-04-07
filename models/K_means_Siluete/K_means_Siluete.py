from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer
import matplotlib.pyplot as plt


def calculate_plot_Kmeans(M, iteration_size):
    kmeans = KMeans(n_clusters=2)
    lst_labels = []
    lst_kmeans = []

    for i in range(int(len(M)/iteration_size)):
        begin = i*iteration_size
        end = (i+1)*iteration_size
        labels = kmeans.fit_predict(M[begin:end])
        centers = kmeans.cluster_centers_

        # check if the anchors are in the same cluster
        if labels[0] == labels[1]:
            raise Exception('The anchors are in the same cluster')

        # plot the anchors
        plt.scatter(M[begin, 0], M[begin, 1], c='green', s=200, alpha=0.5)
        plt.scatter(M[begin+1, 0], M[begin+1, 1], c='red', s=200, alpha=0.5)
        # plot the rest of the data
        plt.scatter(M[begin:end, 0],
                    M[begin:end, 1],
                    c=labels[:], s=50, cmap='viridis')
        # plot the center of the data
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.3)

        lst_labels.append(labels)
        lst_kmeans.append(kmeans)

        plt.show()

    return lst_labels, lst_kmeans


def silhouette(M, labels, kmeans, iteration_size):

    for i in range(int(len(M)/iteration_size)):
        score = silhouette_score(M[i*iteration_size:(i+1)*iteration_size],
                                 labels=labels[i], metric='euclidean')
        print("The Silhouette score is :" + str(score))

        visualizer = SilhouetteVisualizer(kmeans[i], colors='yellowbrick')
        visualizer.fit(M[i*iteration_size:(i+1)*iteration_size])
        visualizer.show()

    return score# the last score