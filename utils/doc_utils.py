import os
import sys

from typing import List



class Documents_utils():
    working_dir = sys.path[0] if 'Ghazali' in sys.path[0] else sys.path[1]

    c1 = '\\'.join([working_dir, 'Books', 't1'])
    c2 = '\\'.join([working_dir, 'Books', 't2'])
    c3 = '\\'.join([working_dir, 'Books', 't3'])

    @staticmethod
    def get_list_of_docs_files(folder_path: str) -> List[str]:
        """ this function get a folder path and return list of docs with name"""
        try:
            list_of_files = os.listdir(path=folder_path)
        except:
            return
        doc_list: List[str] = []
        for file in list_of_files:
            if file.endswith('.txt'):
                doc_list.append(file)
        return doc_list

    @staticmethod
    def read_doc_file(file_path: str) -> str:
        f = open(file_path, 'r', encoding='utf-8')
        data_in_file = f.read()
        return data_in_file

    @staticmethod
    def get_list_of_books(folder_path: str):
        meta_data = []
        books_name: List[str] = Documents_utils.get_list_of_docs_files(folder_path=folder_path)
        for name in books_name:
            curr_book_path = os.path.join(folder_path, name)
            meta_data.append(Documents_utils.read_doc_file(file_path=curr_book_path))


        return meta_data
