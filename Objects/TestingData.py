
class TestingData:

    def __init__(self, c3, c3_books_names, c1_anchor_name, c2_anchor_name, c1_test_names, c2_test_names, c3_test_names):

        self.c1_anchor_name = c1_anchor_name
        self.c2_anchor_name = c2_anchor_name
        self.c1_test_names = c1_test_names
        self.c2_test_names = c2_test_names
        self.c3_test_names = c3_test_names

        self.anchor_c1 = []
        self.anchor_c2 = []
        self.c1_test = []
        self.c2_test = []
        self.c3_test = []

        for idx, book_name in enumerate(c3_books_names):
            """Get the c1_anchor data"""
            for idn, anchor_book in enumerate(c1_anchor_name):
                if anchor_book == book_name[:-4]:
                    self.anchor_c1.append(c3[idx])
            """Get the c2_anchor data"""
            for idn, anchor_book in enumerate(c2_anchor_name):
                if anchor_book == book_name[:-4]:
                    self.anchor_c2.append(c3[idx])
            """Get the c1_test data"""
            for idn, test_book in enumerate(c1_test_names):
                if test_book == book_name[:-4]:
                    self.c1_test.append(c3[idx])
            """Get the c2_test data"""
            for idn, test_book in enumerate(c2_test_names):
                if test_book == book_name[:-4]:
                    self.c2_test.append(c3[idx])
            """Get the c3_test data"""
            for idn, test_book in enumerate(c3_test_names):
                if test_book == book_name[:-4]:
                    self.c3_test.append(c3[idx])

        self.iteration_size = len(c3)



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
                print("%14.2f, %-14.2f|" % (M[i * self.iteration_size + j][0],
                                        M[i * self.iteration_size + j][1]), end="")

            # new line
            print()
            if len(labels)>0:
                for j in range(self.iteration_size):
                    print("%-30d|" % (labels[i * self.iteration_size + j]), end="")

            # new line
            print()