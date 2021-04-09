


class TestingData:

    def __init__(self, c1, c2, c3):
        self.c1 = c1[1:]
        self.c2 = c2[1:]
        self.c3 = c3[1:]
        self.c1_anchor = [c1[0]]
        self.c2_anchor = [c2[0]]
        self.iteration_size = len(self.c1)+\
                              len(self.c2)+\
                              len(self.c3)+\
                              len(self.c1_anchor)+\
                              len(self.c2_anchor)



    def show_results_of_tests(self, M):
        for i in range(int(len(M) / self.iteration_size)):
            print("Iteration Num:{}".format(int(i)))

            # -------------------------------   header   ------------------------------------
            # anchor_c1
            for k in range(len(self.c1_anchor)): print("%-8s%2d|" % ("anc_CL1:", k), end="")
            # anchor_c2
            for k in range(len(self.c2_anchor)): print("%-8s%2d|" % ("anc_CL2:", k), end="")
            # c1
            for k in range(len(self.c1)): print("%-8s%2d|" % ("CL1:", k), end="")
            # c2
            for k in range(len(self.c2)): print("%-8s%2d|" % ("CL2:", k), end="")
            # c3
            for k in range(len(self.c3)): print("%-8s%2d|" % ("CL3:", k), end="")

            separator = "-" * 100
            print("\n" + separator)

            for j in range(self.iteration_size):
                print("%3.2f, %3.2f|" % (M[i * self.iteration_size + j][0],
                                        M[i * self.iteration_size + j][1]), end="")

            # new line
            print()