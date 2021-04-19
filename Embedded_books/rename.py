import os
from utils.doc_utils import Documents_utils

curr_dir = Documents_utils.project_working_dir

c1 = '\\'.join([curr_dir, 'Embedded_books', 'c1'])
c2 = '\\'.join([curr_dir, 'Embedded_books', 'c2'])
c3 = '\\'.join([curr_dir, 'Embedded_books', 'c3'])



def rename_folder_files(folder_path):
    try:
        list_of_files = os.listdir(path=folder_path)
    except Exception as e:
        print(e)
        return
    doc_list = []
    for file in list_of_files:
        if file.endswith('.npy'):
            os.rename(folder_path+"\\"+file, folder_path+"\\"+file[:-4]+"_200"+file[-4:])
            print(file[:-4]+"_200"+file[-4:])


rename_folder_files(c3)