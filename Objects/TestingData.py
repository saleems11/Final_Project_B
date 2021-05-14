from Objects.Book import Book
import numpy as np

class TestingData:
    anchors_names = {'c1_test': 'c1_test',
                     'c2_test': 'c2_test',
                     'c3_test': 'c3_test',
                     'c1_anchor': 'c1_anchor',
                     'c2_anchor': 'c2_anchor'}

    def __init__(self, c3, c3_books_names, c1_anchor_name, c2_anchor_name, c1_test_names, c2_test_names, c3_test_names):

        self.books = []

        self.c3_books_names = c3_books_names
        self.c1_anchor_name = c1_anchor_name
        self.c2_anchor_name = c2_anchor_name
        self.c1_test_names = c1_test_names
        self.c2_test_names = c2_test_names
        self.c3_test_names = c3_test_names

        self.sort_data_to_clusters(c3=c3)

        self.anchor_c1 = []
        self.anchor_c2 = []
        self.c1_test = []
        self.c2_test = []
        self.c3_test = []

        self.set_clusters_image()

        # set the anchor and testing data pointers

        # for idx, book_name in enumerate(c3_books_names):
        #     """Get the c1_anchor data"""
        #     for idn, anchor_book in enumerate(c1_anchor_name):
        #         if anchor_book == book_name[:-4]:
        #             self.anchor_c1.append(c3[idx])
        #     """Get the c2_anchor data"""
        #     for idn, anchor_book in enumerate(c2_anchor_name):
        #         if anchor_book == book_name[:-4]:
        #             self.anchor_c2.append(c3[idx])
        #     """Get the c1_test data"""
        #     for idn, test_book in enumerate(c1_test_names):
        #         if test_book == book_name[:-4]:
        #             self.c1_test.append(c3[idx])
        #     """Get the c2_test data"""
        #     for idn, test_book in enumerate(c2_test_names):
        #         if test_book == book_name[:-4]:
        #             self.c2_test.append(c3[idx])
        #     """Get the c3_test data"""
        #     for idn, test_book in enumerate(c3_test_names):
        #         if test_book == book_name[:-4]:
        #             self.c3_test.append(c3[idx])

        self.iteration_size = len(c3)

    def set_clusters_image(self):
        for idx in range(len(self.books)):
            if self.books[idx].cluster == self.anchors_names['c1_anchor']:
                self.anchor_c1.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c2_anchor']:
                self.anchor_c2.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c1_test']:
                self.c1_test.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c2_test']:
                self.c2_test.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c3_test']:
                self.c3_test.append(self.books[idx])

    def sort_data_to_clusters(self, c3):
        for idx, book_name in enumerate(self.c3_books_names):
            """Get the c1_anchor data"""
            for idn, anchor_book in enumerate(self.c1_anchor_name):
                if anchor_book == book_name:
                    self.books.append(Book(book_name=anchor_book,
                                           embedded_data=c3[idx],
                                           cluster=self.anchors_names['c1_anchor']))
            """Get the c2_anchor data"""
            for idn, anchor_book in enumerate(self.c2_anchor_name):
                if anchor_book == book_name:
                    self.books.append(Book(book_name=anchor_book,
                                           embedded_data=c3[idx],
                                           cluster=self.anchors_names['c2_anchor']))
            """Get the c1_test data"""
            for idn, test_book in enumerate(self.c1_test_names):
                if test_book == book_name:
                    self.books.append(Book(test_book,
                                           c3[idx],
                                           self.anchors_names['c1_test']))
            """Get the c2_test data"""
            for idn, test_book in enumerate(self.c2_test_names):
                if test_book == book_name:
                    self.books.append(Book(book_name=test_book,
                                           embedded_data=c3[idx],
                                           cluster=self.anchors_names['c2_test']))
            """Get the c3_test data"""
            for idn, test_book in enumerate(self.c3_test_names):
                if test_book == book_name:
                    self.books.append(Book(book_name=test_book,
                                           embedded_data=c3[idx],
                                           cluster=self.anchors_names['c3_test']))

    def show_results_of_tests(self, M, labels):
        for i in range(int(len(M) / self.iteration_size)):
            print("Iteration Num:{}".format(int(i)))

            # -------------------------------   header   ------------------------------------
            # anchor_c1
            for idx, file_name in enumerate(self.c1_anchor_name):
                print("%-8s%-20s%2d|" % ("anc_CL1:", file_name[:20], idx), end="")
            # anchor_c2
            for idx, file_name in enumerate(self.c2_anchor_name):
                print("%-8s%-20s%2d|" % ("anc_CL2:", file_name[:20], idx), end="")
            # c1 test
            for idx, file_name in enumerate(self.c1_test_names):
                print("%-8s%-20s%2d|" % ("CL1:", file_name[:20], idx), end="")
            # c2 test
            for idx, file_name in enumerate(self.c2_test_names):
                print("%-8s%-20s%2d|" % ("CL2:", file_name[:20], idx), end="")
            # c3 test
            for idx, file_name in enumerate(self.c3_test_names):
                print("%-8s%-20s%2d|" % ("CL3:", file_name[:20], idx), end="")

            separator = "-" * 100
            print("\n" + separator)

            for j in range(self.iteration_size):
                print("%30.2f|" % M[i * self.iteration_size + j], end="")

            # new line
            print()
            if len(labels) > 0:
                for j in range(self.iteration_size):
                    print("%-30d|" % (labels[i * self.iteration_size + j]), end="")

            # new line
            print()

    def get_error_bar_data(self):
        books_names = []
        books_mean_values_over_all_iter = []
        books_error_up_values_over_all_iter = []
        books_error_down_values_over_all_iter = []

        c1_mean_val = 0
        c2_mean_val = 0
        c1_labels_count = 0
        c2_labels_count = 0
        mean_val = 0

        for book in self.books:
            most_min, most_max, mean_over_iterations = book.prediction_res_over_all_iter()

            mean_val += mean_over_iterations

            for label in book.label:
                if label == 0:
                    c1_mean_val += mean_over_iterations
                    book.total_c1_hits += 1
                elif label == 1:
                    c2_mean_val += mean_over_iterations
                    book.total_c2_hits += 1

            c1_labels_count += book.total_c1_hits
            c2_labels_count += book.total_c2_hits

            books_names.append(book.book_name[:20])
            books_mean_values_over_all_iter.append(mean_over_iterations)
            books_error_down_values_over_all_iter.append(abs(most_min - mean_over_iterations))
            books_error_up_values_over_all_iter.append(abs(most_max - mean_over_iterations))

        mean_val /= len(self.books)

        if c1_labels_count != 0:
            c1_mean_val = c1_mean_val / c1_labels_count
        if c2_labels_count != 0:
            c2_mean_val = c2_mean_val / c2_labels_count

        return books_names,\
               books_mean_values_over_all_iter, \
               books_error_down_values_over_all_iter, \
               books_error_up_values_over_all_iter, \
               books_mean_values_over_all_iter, \
               c1_mean_val,\
               c2_mean_val, \
               mean_val


    def set_book_mean_prediction_val_over_iter(self, book):
        mean_val = np.zeros((len(book.predictions_res_over_iter[0])), dtype='f')
        for predictions in book.predictions_res_over_iter:
            mean_val = np.add(mean_val, predictions[:, 0])

        book.mean_of_mean_prediction_res_over_iter = np.divide(mean_val, len(book.predictions_res_over_iter))


    def get_book(self, book_name):
        for book in self.books:
            if book.book_name == book_name:
                return book
        # or raise exception
        return None
