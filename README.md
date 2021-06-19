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
RUN the GUI.py file found in GUI\GUI.py.
USE the dataset found in the project in Books directory which contains t1\t2\t3.
t1: Al-Ghazali data.
t2: Pseduo Al-Ghazali data.
t3: Testing dataset.

## Info about the dataset of testing(found in t3)
➢ Books are written by Al-Ghazali:
0) Al-Mankhul min Taliqat al-Usul* (an anchor);
1) Al Mustasfa min ilm al-Usul*;
2) Fada'ih al-Batiniyya wa Fada'il al-Mustazhiriyy*;.
3) Faysal at-Tafriqa Bayna al-Islam wa al-Zandaqa*;
4) Kitab al-iqtisad fi al-i'tiqad*;
5) Kitab Iljam Al- Awamm an Ilm Al-Kalam*;
6) Tahafut al-Falasifa;
➢ Texts agreed not written by Al Ghazali ("Pseudo- Ghazali):
7) Ahliyi al-Madnun bihi ala ghayri*;
8) Kimiya-yi Sa'ādat* (an anchor);
➢ A book with questionable authorship:
9) Mishakat al-Anwar

## Git LFS
The Project uses Git LFS, for the trained models(Elmo).
The link for how to use Git LFS:
[GIT_LFS](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-migrate.1.ronn?utm_source=gitlfs_site&utm_medium=doc_man_migrate_link&utm_campaign=gitlfs)
