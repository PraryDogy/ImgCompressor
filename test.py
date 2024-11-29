import os
from cfg import Cfg

def process_files_and_folders(base_path, data: dict[list[dict]]):
    named_folders: list[dict] = data.get(Cfg.NAMED_FOLDER, [])
    file_folders: list[dict] = data.get(Cfg.FILE_FOLDER, [])

    compress: dict[str, int] = {}

    for root, dirs, files in os.walk(base_path):
        for dir in dirs:

            # мы проверяем все именованные папки
            for data_dict in named_folders:
                dir_src = os.path.join(root, dir)
                if dir == data_dict.get(Cfg.SRC):
                    # сжимаем все фотки внутри этой папки
                    for root_, dirs_, files_ in os.walk(dir_src):
                        for file_ in files_:
                            img_src = os.path.join(root_, file_)
                            if os.path.isfile(img_src) and img_src.endswith(Cfg.IMG_EXTS):
                                compress[img_src] = data_dict.get(Cfg.MAX_SIZE_KB)

            # мы проверяем конкретно указанные папки
            for data_dict in file_folders:
                dir_src = os.path.join(root, dir)
                if dir_src == data_dict.get(Cfg.SRC):
                    # сжимаем все фотки внутри этой папки
                    for root_, dirs_, files_ in os.walk(dir_src):
                        for file_ in files_:
                            img_src = os.path.join(root_, file_)
                            if os.path.isfile(img_src) and img_src.endswith(Cfg.IMG_EXTS):
                                compress[img_src] = data_dict.get(Cfg.MAX_SIZE_KB)

        for file in files:

            for data_dict in file_folders:
                file_src = os.path.join(root, file)
                if file_src == data_dict.get(Cfg.SRC):
                    if os.path.isfile(file_src) and file_src.endswith(Cfg.IMG_EXTS):
                        compress[file_src] = data_dict.get(Cfg.MAX_SIZE_KB)

    for k, v in compress.items():
        print(k, v)


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
