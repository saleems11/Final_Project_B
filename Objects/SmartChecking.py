class SmartChecking:

    def __init__(self):
        self.tweet_size_options = [200, 300]
        self.bi_lstm_hidden_state_size_min = 32
        self.bi_lstm_hidden_state_size_max = 32+3*64
        self.bi_lstm_hidden_state_size_jump = 64
        self.learning_rate_max = 0.006
        self.learning_rate_min = 0.001
        self.learning_rate_jump = 0.0015
        self.fully_connected_layer_min = 20
        self.fully_connected_layer_max = 60
        self.fully_connected_layer_jump = 20
        self.batch_size_min = 128
        self.batch_size_max = 320
        self.batch_size_jump = 64
        self.epoch_min = 10
        self.epoch_max = 25
        self.epoch_jump = 5
        self.drop_out_min = 0.3
        self.drop_out_max = 0.6
        self.drop_out_jump = 0.1
        """
        0 tweet_size_options
        1 bi_lstm_hidden_state_size
        2 learning_rate
        3 fully_connected_layer
        4 batch_size
        5 epoch
        6 drop_out"""
        self.num_of_param = 7
        self.options_state = [1, 3, 2, 1, 0, 0, 0]
        self.each_parameter_numof_options = [0] * self.num_of_param

        self.set_parameters_options_number()


    def set_parameters_options_number(self):
        self.each_parameter_numof_options[0] = len(self.tweet_size_options)
        self.each_parameter_numof_options[1] = int((self.bi_lstm_hidden_state_size_max -
                                                             self.bi_lstm_hidden_state_size_min) /
                                                            self.bi_lstm_hidden_state_size_jump) + 1

        self.each_parameter_numof_options[2] = int((self.learning_rate_max -
                                                             self.learning_rate_min) /
                                                            self.learning_rate_jump) + 1

        self.each_parameter_numof_options[3] = int((self.fully_connected_layer_max -
                                                             self.fully_connected_layer_min) /
                                                            self.fully_connected_layer_jump) + 1

        self.each_parameter_numof_options[4] = int((self.batch_size_max -
                                                             self.batch_size_min) /
                                                            self.batch_size_jump) + 1

        self.each_parameter_numof_options[5] = int((self.epoch_max -
                                                             self.epoch_min) /
                                                            self.epoch_jump) + 1

        self.each_parameter_numof_options[6] = int((self.drop_out_max -
                                                             self.drop_out_min) /
                                                            self.drop_out_jump) + 1

        for i in range(len(self.each_parameter_numof_options)):
            self.options_state[i] = self.options_state[i]%self.each_parameter_numof_options[i]


    def new_parameters_values(self):
        print(self.options_state)

        res = [self.tweet_size_options[self.options_state[0]],

                self.bi_lstm_hidden_state_size_min +
                (self.bi_lstm_hidden_state_size_jump *
                 self.options_state[1]),

                self.learning_rate_min +
                (self.learning_rate_jump *
                 self.options_state[2]),

                self.fully_connected_layer_min +
                (self.fully_connected_layer_jump *
                 self.options_state[3]),

                self.batch_size_min +
                (self.batch_size_jump *
                 self.options_state[4]),

                self.epoch_min +
                (self.epoch_jump *
                 self.options_state[5]),

                self.drop_out_min +
                (self.drop_out_jump *
                 self.options_state[6])
                ]

        # update options state
        for i in range(len(self.options_state)):
            self.options_state[i] += 1
            if self.options_state[i] >= self.each_parameter_numof_options[i]:
                self.options_state[i] = 0
            else: break



        print(res)
        return res