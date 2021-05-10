class Parameters:
    """A Class that contain the parameters for the model"""
    # AraVec_embedding_vector_lenght=100
    # LSTM_hidden_state_dimension = 200
    # Number_of_units_in fully_connected_layer = 30
    # Dropout_rate = 0.3
    # Learning_rate = 0.001
    # Number_of_epochs = 10
    # Batch_size= 50
    # Niter_iterations_number=20
    # L=128
    # l0=64
    # undersampling_rate = 2
    # multiplying_rate =3
    # Accuracy_threshold=0.96
    # Silhouette_threshold=0.75
    def __init__(self, lstm_hidden_state_size: int, fully_connect_layer: int,
                 drop_out:float, learning_rate:float, number_of_epoch:int, batch_size:int,
                 number_of_iteration: int, tweet_length: int, undersampling_rate: int = 2,
                 multiplying_rate: int = 3, accuracy_threshold: float = 0.96, silhouette_threshold: float = 0.75,
                 optimizer: str = 'Adam', activation_function: str = 'RElu'):
        self.lstm_hidden_state_size = lstm_hidden_state_size
        self.fully_connect_layer = fully_connect_layer
        self.drop_out = drop_out
        self.learning_rate = learning_rate
        self.number_of_epoch = number_of_epoch
        self.batch_size = batch_size
        self.number_of_iteration = number_of_iteration

        self.undersampling_rate = undersampling_rate
        self.multiplying_rate = multiplying_rate
        self.accuracy_threshold = accuracy_threshold
        self.silhouette_threshold = silhouette_threshold
        self.optimizer = optimizer
        self.activation_function = activation_function
        self.tweet_length = tweet_length