import numpy as np

class Book:

    def __init__(self, book_name, embedded_data, cluster):
        self.book_name = book_name
        self.embedded_data = embedded_data
        self.cluster = cluster

        self.predictions_res_over_iter = []
        self.mean_prediction_res_over_iter = []
        self.min_predictions_res_over_iter = []
        self.max_predictions_res_over_iter = []

        self.total_c1_hits = 0
        self.total_c2_hits = 0

        self.label = []
        self.mean_of_mean_prediction_res_over_iter = None

    def add_prediction_res(self, predictions, mean_predictions):
        self.predictions_res_over_iter.append(predictions)
        self.mean_prediction_res_over_iter.append(mean_predictions)
        self.min_predictions_res_over_iter.append(predictions.min())
        self.max_predictions_res_over_iter.append(predictions.max())

    def prediction_res_over_all_iter(self):
        most_min = min(self.mean_prediction_res_over_iter)
        most_max = max(self.mean_prediction_res_over_iter)

        mean_over_iterations = sum(self.mean_prediction_res_over_iter)/len(self.mean_prediction_res_over_iter)
        return most_min, most_max, mean_over_iterations

    def mean_prediction_over_iteration(self):
        mean_over_iterations = np.zeros(self.predictions_res_over_iter[0].shape[0])
        for prediction_res in self.predictions_res_over_iter:
            mean_over_iterations += prediction_res
        mean_over_iterations = mean_over_iterations/len(self.predictions_res_over_iter)
        return mean_over_iterations

    def add_label(self, label):
        self.label.append(label)

    @staticmethod
    def get_book_details_as_string(book_name:str, index:int, cluster:str) -> str:
        return "[{0}]({1}) {2}".format(index, cluster, book_name)
