# Attributing-authorship-of-Ghazali-book-using-Bi-Directional-LSTM
The project is splited into three parts:


## Word Embedding (Elmo):
this model is a deep contextualized word representation that models both complex characteristics of word use, and how these uses vary across linguistic contexts. These word    vectors are learned functions of the internal states of a deep bidirectional language model (bi-LSTM) with this model can predict the word (after and before) after choosing one from the bag, ELMo is pre-trained on a large text corpus

## BI-Directional LSTM:
LSTMs train two instead of one input sequence. The first on the input sequence as-is and the second on a reversed copy of the input sequence. 
  
## Balancing Method:
There is a significant difference between the total size of "Al-Ghazali, Pseudo Al-Ghazali" books, that is due to the large volume of  Al-Ghazālī's "Iḥyā ulūm al-dīn" which construct the main class, such a situation lead to unbalanced classification.
Due to that, the minority group will be ignored, caused by the bias towards the majority, to solve this problem there is a need to reduce the size of the majority group and increase the size of the minority before training the model. 
considering the two datasets D1 and D2 that is |D1|>|D2|

## Runing the model 
RUN the GUI.py file.

## Git LFS
The Project uses Git LFS, for the trained models(Elmo).
The link for how to use Git LFS:
[GIT_LFS](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-migrate.1.ronn?utm_source=gitlfs_site&utm_medium=doc_man_migrate_link&utm_campaign=gitlfs)
