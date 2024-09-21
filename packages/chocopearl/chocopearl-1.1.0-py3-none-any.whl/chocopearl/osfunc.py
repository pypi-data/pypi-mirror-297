import os

def list_txt(path=None):
    if path is None:
        path=os.getcwd()
    txt_list = []
    txtpath_list = []
    for name in os.listdir(path):
        if name.endswith('.txt'):
            full_path = os.path.join(path, name)
            txt_list.append(name)
            txtpath_list.append(full_path)
    return txt_list,txtpath_list

def list_pickle(path=None):
    if path is None:
        path=os.getcwd()
    pickle_list = []
    picklepath_list = []
    for name in os.listdir(path):
        if name.endswith('.pickle'):
            full_path = os.path.join(path, name)
            pickle_list.append(name)
            picklepath_list.append(full_path)
    return pickle_list,picklepath_list

def list_files(path=None,extension=None):
    if path is None:
        path=os.getcwd()
    filenames_list = []
    filepaths_list = []
    if extension is None:
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            filenames_list.append(name)
            filepaths_list.append(full_path)
    else:
        n=len(extension)
        for name in os.listdir(path):
            if name.endswith(extension):
                full_path = os.path.join(path, name)
                filenames_list.append(name)
                filepaths_list.append(full_path)
    return filenames_list,filepaths_list

def list_directories(parent_directory=None):
    if parent_directory is None:
        parent_directory=os.getcwd()
    directories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
    return directories

