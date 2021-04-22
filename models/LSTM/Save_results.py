def save_history_data(tweet_length, epoch, batch_size, drop_out, bi_lstm_hidden_state_size,
                      history, learning_rate, embedding_size, score, iteration_number):
    # file for saving the result and the parameters
    file = open("result_checks.txt", "a")

    file.write("-- tweet len:{0}, epochs:{1}, batch_size={2}, drop_out={3}, bi_lstm_hidden_state_size:{4}"
               "\naccuracy:{5}, validation accuracy: {6}, learning rate: {7}, embedding_size: {8}\n"
               "The Silhouette score: {9}, iteration number: {10}\n".format(
        tweet_length, epoch, batch_size, drop_out,
        bi_lstm_hidden_state_size, sum(history.history['accuracy']) / len(history.history['accuracy']),
                                   sum(history.history['val_accuracy']) / len(history.history['val_accuracy']),
        learning_rate,
        embedding_size, score, iteration_number))
    file.close()