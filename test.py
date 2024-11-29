import os
from cfg import Cfg

def compress_named_folders(root, dirs, named_folders):
    compress = {}
    for dir in dirs:
        for data_dict in named_folders:
            if dir == data_dict.get(Cfg.SRC):
                dir_src = os.path.join(root, dir)
                compress.update(compress_images_in_directory(dir_src, data_dict.get(Cfg.MAX_SIZE_KB)))
    return compress

def compress_specific_folders(root, dirs, file_folders):
    compress = {}
    for dir in dirs:
        for data_dict in file_folders:
            dir_src = os.path.join(root, dir)
            if dir_src == data_dict.get(Cfg.SRC):
                compress.update(compress_images_in_directory(dir_src, data_dict.get(Cfg.MAX_SIZE_KB)))
    return compress

def compress_specific_files(root, files, file_folders):
    compress = {}
    for file in files:
        file_src = os.path.join(root, file)
        for data_dict in file_folders:
            if file_src == data_dict.get(Cfg.SRC) and os.path.isfile(file_src):
                compress[file_src] = data_dict.get(Cfg.MAX_SIZE_KB)
    return compress

def compress_images_in_directory(directory, max_size_kb):
    compress = {}
    for root_, _, files_ in os.walk(directory):
        for file_ in files_:
            img_src = os.path.join(root_, file_)
            if os.path.isfile(img_src) and img_src.endswith(Cfg.IMG_EXTS):
                compress[img_src] = max_size_kb
    return compress

def process_files_and_folders(base_path, data: dict[list[dict]]):
    named_folders = data.get(Cfg.NAMED_FOLDER, [])
    file_folders = data.get(Cfg.FILE_FOLDER, [])

    compress = {}
    for root, dirs, files in os.walk(base_path):
        compress.update(compress_named_folders(root, dirs, named_folders))
        compress.update(compress_specific_folders(root, dirs, file_folders))
        compress.update(compress_specific_files(root, files, file_folders))

    for img_src, max_size_kb in compress.items():
        print(img_src, max_size_kb)

# Пример использования
base_path = '/Users/Loshkarev/Desktop/test'

data = {
    Cfg.NAMED_FOLDER: [
        {'src': 'ХО', 'max_size_kb': 100},
        {'src': 'ГО', 'max_size_kb': 50}
    ],
    Cfg.FILE_FOLDER: [
        {'src': '/Users/Loshkarev/Desktop/test/Test 2', 'max_size_kb': 666}, 
        {'src': '/Users/Loshkarev/Desktop/test/Test/file 1.jpg', 'max_size_kb': 123}
    ],
    Cfg.MAIN_FOLDER: [
        {"src": None, "max_size_kb": 1000}
    ]
}

process_files_and_folders(base_path, data)
