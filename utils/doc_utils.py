import os
import sys

from typing import List

working_dir = sys.path[1]
c1 = '\\'.join([working_dir, 'Books', 't1'])
c2 = '\\'.join([working_dir, 'Books', 't2'])
c3 = '\\'.join([working_dir, 'Books', 't3'])


def get_list_of_docs_files(folder_path: str) -> List[str]:
    """ this function get a folder path and return list of docs with name"""
    list_of_files = os.listdir(path=folder_path)
    doc_list: List[str] = []
    for file in list_of_files:
        if file.endswith('.txt'):
            doc_list.append(file)
    return doc_list


def read_doc_file(file_path: str) -> str:
    f = open(file_path, 'r', encoding='utf-8')
    data_in_file = f.read()
    print(data_in_file)
    return data_in_file


def get_list_of_books(folder_path: str):
    meta_data = []
    books_name: List[str] = get_list_of_docs_files(folder_path=folder_path)
    print(folder_path)
    print(books_name)
    for name in books_name:
        curr_book_path = os.path.join(folder_path, name)
        meta_data.append(read_doc_file(file_path=curr_book_path))
    return meta_data


print(get_list_of_books(folder_path=c1))
