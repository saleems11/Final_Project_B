from Objects.Book import Book
import numpy as np

class TestingData:
    """ A Class for managing the prediction result according to the cluster and the  each book name"""
    anchors_names = {'c1_test': 'c1 test',
                     'c2_test': 'c2 test',
                     'unknown_author': 'unknown author',
                     'c1_anchor': 'c1 anchor',
                     'c2_anchor': 'c2 anchor'}

    def __init__(self, c3, c3_books_names, c1_anchor_name, c2_anchor_name, c1_test_names, c2_test_names, c3_test_names):
        """ initialize all the cluster books references, and sort each book to the appropriate cluster
        and adding them to the books list
        Receives:
        c3: contain all the embedded data in testing data
        c3_books_names: [str] list of c3 testing data(list of all the books names in c1_anchor_name, c2_anchor_name,
         c1_test_names, c2_test_names, c3_test_names)
        c1_anchor_name: [str] list of books as anchor's in c1
        c2_anchor_name: [str] list of books as anchor's in c2
        c1_test_names: [str] list of books for testing as c1
        c2_test_names: [str] list of books for testing as c2
        c3_test_names: [str] list of books for testing as testing of unknown data"""
        self.books = []

        self.c3_books_names = c3_books_names
        self.c1_anchor_name = c1_anchor_name
        self.c2_anchor_name = c2_anchor_name
        self.c1_test_names = c1_test_names
        self.c2_test_names = c2_test_names
        self.c3_test_names = c3_test_names

        """ sort the embedding results to the cluster group and create the books objects """
        self.sort_data_to_clusters(c3=c3)
        """ reorder the file according to Zeev paper if all the files exist """
        self.reorder_books()

        self.anchor_c1 = []
        self.anchor_c2 = []
        self.c1_test = []
        self.c2_test = []
        self.c3_test = []

        """ set the clusters pointers lists """
        self.set_clusters_image()

        self.iteration_size = len(c3)

    def reorder_books(self):
        """ reorder the book in the same order as in Zeev papper
        The reordering is done just if the files does exist"""

        books_in_order = ['Al_Mankhul_min_Taliqat_al_Usul.txt', 'Al_Mustasfa_min_ilm_al_Usul.txt',
                          'Fada_ih_al_Batiniyya_wa_Fada_il_al_Mustazhiriyy.txt',
                          'Faysal_at_Tafriqa_Bayna_al_Islam_wa_al_Zandaqa.txt', 'al_iqtisad_fi_al_itiqad.txt',
                          'Iljam_Al_Awamm_an_Ilm_Al_Kalam.txt', 'Tahafut_al_Falasifa.txt',
                          'al_Madnun_bihi_ala_ghayri.txt', 'Kimiya_yi_Saadat.txt', 'Mishakat_al_Anwar.txt']
        if len(self.books) != len(books_in_order):
            return

        temp_books_list = []
        for idx, book_name in enumerate(books_in_order):
            selected_idx = -1
            for j in range(len(self.c3_books_names)):
                if book_name == self.c3_books_names[j]:
                    selected_idx = j
                    break
            if selected_idx != -1:
                temp_books_list.append(self.books[selected_idx])
            else:
                return
        print("HELLOOZ")
        self.books = temp_books_list
        self.c3_books_names = books_in_order

    def set_clusters_image(self):
        """ sort book object into appropriate cluster list according to book cluster """
        for idx in range(len(self.books)):
            if self.books[idx].cluster == self.anchors_names['c1_anchor']:
                self.anchor_c1.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c2_anchor']:
                self.anchor_c2.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c1_test']:
                self.c1_test.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['c2_test']:
                self.c2_test.append(self.books[idx])
            elif self.books[idx].cluster == self.anchors_names['unknown_author']:
                self.c3_test.append(self.books[idx])

    def sort_data_to_clusters(self, c3):
        """ add book object into books list according to book cluster and set each book attributes """
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
                                           cluster=self.anchors_names['unknown_author']))

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
        """ get the needed data for the error bar including for each book the min, max, mean mean
        prediction over of all the iterations and c1, c2 means and the total mean"""
        books_names = []
        books_mean_values_over_all_iter = []
        books_error_up_values_over_all_iter = []
        books_error_down_values_over_all_iter = []

        c1_mean_val = 0
        c2_mean_val = 0
        c1_labels_count = 0
        c2_labels_count = 0
        mean_val = 0

        c1_label = self.anchor_c1[0].label[-1]
        c2_label = self.anchor_c2[0].label[-1]

        for book in self.books:
            # get book (most_min, most_max, mean_over_iterations) of mean prediction result
            most_min, most_max, mean_over_iterations = book.prediction_res_over_all_iter()

            # update all books mean value
            mean_val += mean_over_iterations

            # update for each label added to book the mean value of each cluster
            for label in book.label:
                if label == c1_label:
                    c1_mean_val += mean_over_iterations
                    book.total_c1_hits += 1
                elif label == c2_label:
                    c2_mean_val += mean_over_iterations
                    book.total_c2_hits += 1

            # update the cluster books number clustered to c1,c2
            c1_labels_count += book.total_c1_hits
            c2_labels_count += book.total_c2_hits

            # calculate mean value, error up, error down, and books names
            books_names.append(book.book_name)
            books_mean_values_over_all_iter.append(mean_over_iterations)
            books_error_down_values_over_all_iter.append(abs(most_min - mean_over_iterations))
            books_error_up_values_over_all_iter.append(abs(most_max - mean_over_iterations))

        mean_val /= len(self.books)

        # calculate the mean of each cluster
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

    def get_books_embedding_data(self) -> []:
        """ get books embedding data as list"""
        embedded_book_data_list = []
        for book in self.books:
            embedded_book_data_list.append(book.embedded_data)
        return embedded_book_data_list

    def get_book(self, book_name) -> Book:
        """ get book object by name """
        for book in self.books:
            if book.book_name == book_name:
                return book
        # raise exception
        raise Exception("book name: %s cloud not be found" % book_name)

    def get_book_cluster(self, book_name) -> str:
        """ find the book and return his cluster """
        for book in self.books:
            if book.book_name == book_name:
                return book.cluster
        # or raise exception
        return ''
