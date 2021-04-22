from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer
import matplotlib.pyplot as plt

from Exceptions.Exceptions import AnchorsInSameCluster, SilhouetteBellowThreshold


def calculate_plot_Kmeans(M, iteration_size, testing_data):
    kmeans = KMeans(n_clusters=2)

    labels = kmeans.fit_predict(M)
    centers = kmeans.cluster_centers_

    # check if the anchors are in the same cluster
    for i in range(int(len(M) / iteration_size)):
        # check if all c1 anchors are in the same cluster
        for j in range(1, len(testing_data.anchor_c1)):
            if labels[j - 1] != labels[j]: raise AnchorsInSameCluster('The anchors are in the same cluster')
        # check if all c2 anchors are in the same cluster
        for j in range(len(testing_data.anchor_c1) + 1, len(testing_data.anchor_c1) + len(testing_data.anchor_c2)):
            if labels[j - 1] != labels[j]: raise AnchorsInSameCluster('The anchors are in the same cluster')
        # check if all c1 and c2 are in different cluster
        if labels[0] == labels[len(testing_data.anchor_c1)]: raise AnchorsInSameCluster('The anchors are in the same cluster')

    # create new figure
    plt.figure()

    # plot the anchors
    for i in range(int(len(M) / iteration_size)):
        plt.scatter(M[i * iteration_size, 0], M[i * iteration_size, 1], c='green', s=200, alpha=0.5)
        plt.scatter(M[i * iteration_size + 1, 0], M[i * iteration_size + 1, 1], c='red', s=200, alpha=0.5)
    # plot the rest of the data
    plt.scatter(M[:, 0], M[:, 1], c=labels[:], s=50, cmap='viridis')
    # plot the center of the data
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.3)

    plt.show(block=False)

    return labels, kmeans

    # lst_labels = []
    # lst_kmeans = []
    #
    # for i in range(int(len(M) / iteration_size)):
    #     begin = i * iteration_size
    #     end = (i + 1) * iteration_size
    #     labels = kmeans.fit_predict(M[begin:end])
    #     centers = kmeans.cluster_centers_
    #
    #     # check if the anchors are in the same cluster
    #     if labels[0] == labels[1]:
    #         raise Exception('The anchors are in the same cluster')
    #
    #     # plot the anchors
    #     plt.scatter(M[begin, 0], M[begin, 1], c='green', s=200, alpha=0.5)
    #     plt.scatter(M[begin + 1, 0], M[begin + 1, 1], c='red', s=200, alpha=0.5)
    #     # plot the rest of the data
    #     plt.scatter(M[begin:end, 0],
    #                 M[begin:end, 1],
    #                 c=labels[:], s=50, cmap='viridis')
    #     # plot the center of the data
    #     plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.3)
    #
    #     lst_labels.append(labels)
    #     lst_kmeans.append(kmeans)
    #
    #     plt.show(block=False)
    #
    # return lst_labels, lst_kmeans


def silhouette(M, labels, kmeans, iteration_size, silhouette_threshold):
    score = silhouette_score(M, labels=labels, metric='euclidean')
    if score < silhouette_threshold:
        raise SilhouetteBellowThreshold("The silhouette accuracy is smaller than silhouette_threshold"
                                        "silhouette score is ={0}, but silhouette_threshold ={1}".format(
                                        score, silhouette_threshold), silhouette_val=score
                                        )

    print("The Silhouette score is :" + str(score))

    # create new figures
    plt.figure()
    visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')
    visualizer.fit(M)
    visualizer.show()

    # for i in range(int(len(M) / iteration_size)):
    #     score = silhouette_score(M[i * iteration_size:(i + 1) * iteration_size],
    #                              labels=labels[i], metric='euclidean')
    #     if score < silhouette_threshold:
    #         raise Exception("The silhouette accuracy is smaller than silhouette_threshold"
    #                         "silhouette score is ={0}, but silhouette_threshold ={1}".format(
    #             score, silhouette_threshold
    #         ))
    #
    #     print("The Silhouette score is :" + str(score))
    #
    #     visualizer = SilhouetteVisualizer(kmeans[i], colors='yellowbrick')
    #     visualizer.fit(M[i * iteration_size:(i + 1) * iteration_size])
    #     visualizer.show()

    return round(score, 2)  # the last score
