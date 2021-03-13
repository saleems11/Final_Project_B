import re
import sys

import gensim
from elmoformanylangs import Embedder
import numpy as np

working_dir = sys.path[1]


class Embedding:
    """Procces the data and embed them using AraVec OR ELMo"""

    @staticmethod
    def clean_str(text: str) -> str:
        """Removing any additional characters found in the TEXT, Based on AraVec.\n
         text in str format as a book :parameter\n
         str as a preprocessed book :returns"""

        search = ["أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t',
                  '&quot;', '?', '؟', '!', ':', '(', ')', '']
        replace = ["ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ',
                   ' ؟ ', ' ! ', '', '', '', '']

        # remove tashkeel
        p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        text = re.sub(p_tashkeel, "", text)

        # remove longation
        p_longation = re.compile(r'(.)\1+')
        subst = r"\1\1"
        text = re.sub(p_longation, subst, text)

        text = text.replace('وو', 'و')
        text = text.replace('يي', 'ي')
        text = text.replace('اا', 'ا')

        for i in range(0, len(search)):
            text = text.replace(search[i], replace[i])

        # trim
        text = text.strip()

        return text

    @staticmethod
    def AraVec(striped_text: [str]) -> [[int]]:
        """Embed each word in the book into a Vector in a 100 dimension, based on wikipedia.\n
        Unigram is used, because it Based on single word, unlike N-gram witch based on multiple.
        Addetionaly, skip-gram is used, because it give more than one representation of a word.\n
        a striped text as a striped book :parameter\n
        an embedded value as a array of vectors:returns\n
        There might be in case of word not being found in the directory, so the result len will
        be smaller.\n
        AraVec Github link: https://github.com/bakrianoo/aravec/tree/master/AraVec%202.0"""

        t_model = gensim.models.Word2Vec.load('\\'.join([working_dir, 'models', 'AraVec', 'full_uni_sg_100_wiki.mdl']))
        embedded_book_array = []

        def expect_unwated_words(word: str, unwanted_chars: int):
            try:
                embedded_book_array.append(t_model.wv[word[unwanted_chars:len(word)]])
            except:
                print(word)

        for word in striped_text:
            try:
                embedded_book_array.append(t_model.wv[word])
            except:
                if str(word)[0] == 'و':
                    expect_unwated_words(word=word, unwanted_chars=1)
                elif str(word)[0] == 'وال':
                    expect_unwated_words(word=word, unwanted_chars=3)
        return embedded_book_array

    @staticmethod
    def Elmo(sentences: [str], batch_size=32, output_layer=-1) -> [[int]]:
        """Embedding each word in a sentence according to it's position, each sentence is splitted\n
        The func return the avg of the three layers of the model.\n
        Embeding size is 1024 for each word.\n
        sentences list splited into word:parameter\n
        numpy list of list(the Embedded result of the words):returns\n
        Elmo Github link for multi lang: https://github.com/HIT-SCIR/ELMoForManyLangs"""

        """Embedder(model_dir='/path/to/your/model/', batch_size=64)
        model_dir: the absolute path from the repo top dir to you model dir.
        batch_size: the batch_size you want when the model inference, you can specify
        it properly according to your gpu/cpu ram size. (default: 64)"""
        e = Embedder('\\'.join([working_dir, 'models', 'ArabicElmo']), batch_size=batch_size)

        """def sents2elmo(sents, output_layer=-1):
        sents: the list of lists which store the sentences after segment if necessary.
        output_layer: the target layer to output.
        0 for the word encoder
        1 for the first LSTM hidden layer   
        2 for the second LSTM hidden layer
        -1 for an average of 3 layers. (default)
        -2 for all 3 layers"""
        return e.sents2elmo(sentences, output_layer=output_layer)
