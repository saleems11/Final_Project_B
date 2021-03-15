
import Algs.Embedding as Embedding

class Book:

    def __init__(self, id, name, cl, content):
        self.id = id
        self.name=name
        self.cl=cl
        self.content=content
        self.paragraphs=[]
        self.word_in_paragraph=[]
        self.max_paragraph_len=0
        self.min_paragraph_len=0
        self.avg_paragraph_len=0
        self.total_word_count=0

    def divide_book_to_paragraph(self):
        """"Divide the book into paragraphs"""
        begin=0
        end=begin
        paragraphs = []

        for index in range(len(self.content)):
            if self.content[index] == '.':
                end=index
                paragraphs.append(self.content[begin:end])
                begin=end+1

        self.paragraphs = paragraphs

    def process_book_statistics(self):
        total_words_count=0
        paragraphs_len=[]

        for para in self.paragraphs:
            clean_para = Embedding.Embedding.clean_str(para)
            splited_para = clean_para.split()

            if self.min_paragraph_len==0:
                self.min_paragraph_len=len(splited_para)

            self.min_paragraph_len= min(self.min_paragraph_len, len(splited_para))
            self.max_paragraph_len= max(self.max_paragraph_len, len(splited_para))

            self.word_in_paragraph.append(splited_para)
            total_words_count += len(splited_para)

        self.total_word_count=total_words_count
        self.avg_paragraph_len = total_words_count/len(self.paragraphs)

    def get_book_statistics(self):
        return 'book name: {0}, word count={1}\n' \
               'total paragraphs = {2}, avg words in paragraph = {3}\n' \
               'max paragraph len = {4}, min paragraph len = {5}\n'.format(
            self.name, self.total_word_count, len(self.paragraphs),
            self.avg_paragraph_len, self.max_paragraph_len, self.min_paragraph_len
        )