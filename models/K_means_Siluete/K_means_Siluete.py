from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# from yellowbrick.cluster import SilhouetteVisualizer
# import matplotlib.pyplot as plt
# import numpy as np

from Exceptions.Exceptions import AnchorsInSameCluster, SilhouetteBellowThreshold


def calculate_plot_Kmeans(M, iteration_size, testing_data):
    """ calculate and plot k-means on M matrix, with k=2
    also check if there is two anchor's in the same cluster in the same iteration and over all the iterations
    if two anchors in the  same cluster throw AnchorsInSameCluster Exception """
    # plt.figure()
    kmeans = KMeans(n_clusters=2)

    labels = kmeans.fit_predict(M.reshape(-1, 1))
    centers = kmeans.cluster_centers_

    # update_testing data label
    for idx in range(len(labels)):
        testing_data.books[idx%iteration_size].add_label(labels[idx])

    """ get the labels for C1, C2 """
    c1_label_indexes = []
    c2_label_indexes = []
    for i in range(len(testing_data.books)):
        if testing_data.books[i].cluster == 'c1 anchor':
            c1_label_indexes.append(i)
        elif testing_data.books[i].cluster == 'c2 anchor':
            c2_label_indexes.append(i)

    """ check for each anchor if all his anchor points are in the same cluster """
    for i in range(0, len(M), iteration_size):
        prev = -1
        for idx in c1_label_indexes:
            if prev == -1:
                prev = labels[i+idx]
            elif labels[idx + i] != prev: raise AnchorsInSameCluster('The C1 anchors are in different cluster')
        prev = -1
        for idx in c2_label_indexes:
            if prev == -1:
                prev = labels[i+idx]
            elif labels[idx + i] != prev: raise AnchorsInSameCluster('The C2 anchors are in different cluster')
    """ check if the two cluster have different label """
    if labels[c1_label_indexes[0]] ==labels[c2_label_indexes[0]]:
        raise AnchorsInSameCluster('The anchors are in the same cluster')

    """ 
    # check if the anchors are in the same cluster
    for i in range(int(len(M) / iteration_size)):
        # check if all c1 anchors are in the same cluster
        for j in range(1, len(testing_data.anchor_c1)):
            if labels[j - 1] != labels[j]: raise AnchorsInSameCluster('The C1 anchors are in different cluster')
        # check if all c2 anchors are in the same cluster
        for j in range(len(testing_data.anchor_c1) + 1, len(testing_data.anchor_c1) + len(testing_data.anchor_c2)):
            if labels[j - 1] != labels[j]: raise AnchorsInSameCluster('The C2 anchors are in v cluster')
        # check if all c1 and c2 are in different cluster
        if labels[0] == labels[len(testing_data.anchor_c1)]: raise AnchorsInSameCluster('The anchors are in the same cluster')
    """

    # # plot the anchors
    # for i in range(int(len(M) / iteration_size)):
    #     plt.scatter(M[i * iteration_size], 0, c='green', s=200, alpha=0.5)
    #     plt.scatter(M[i * iteration_size + 1], 0, c='red', s=200, alpha=0.5)
    # # plot the rest of the data
    # plt.scatter(M[:], [0]*len(M), c=labels[:], s=50, cmap='viridis')
    # # plot the center of the data
    # plt.scatter(centers[:], [0]*len(centers), c='black', s=200, alpha=0.3)
    #
    # plt.show(block=False)

    return labels, kmeans



def silhouette(M, labels, kmeans, iteration_size, silhouette_threshold):
    """ calculate the silhouette score using the M Matrix and check the silhouette_threshold, if
    it doesn't achieve it, throw SilhouetteBellowThreshold Exception"""
    score = silhouette_score(M.reshape(-1, 1), labels=labels, metric='euclidean')
    if score < silhouette_threshold:
        raise SilhouetteBellowThreshold("The silhouette accuracy is smaller than silhouette_threshold"
                                        "silhouette score is ={0}, but silhouette_threshold ={1}".format(
                                        score, silhouette_threshold), silhouette_val=score)

    print("The Silhouette score is :" + str(score))

    # create new figures
    # plt.figure()
    # visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')
    # visualizer.fit(M.reshape(-1, 1))
    # visualizer.show()

    return round(score, 2)  # the last score
