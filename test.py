import os
from cfg import Cfg

class FileProcessor:
    def __init__(self, base_path: str, data: dict):
        self.compress = {}
        self.data = data
        self.base_path = base_path

    def named_folders_cmd(self, root, dirs, named_folders: list[dict]):
        for dir in dirs:
            for data_dict in named_folders:
                if dir == data_dict.get(Cfg.SRC):
                    dir_src = os.path.join(root, dir)
                    self.images_in_dir_cmd(dir_src, data_dict.get(Cfg.MAX_SIZE_KB))

    def specific_folders_cmd(self, root, dirs, file_folders: list[dict]):
        for dir in dirs:
            for data_dict in file_folders:
                dir_src = os.path.join(root, dir)
                if dir_src == data_dict.get(Cfg.SRC):
                    self.images_in_dir_cmd(dir_src, data_dict.get(Cfg.MAX_SIZE_KB))

    def specific_files_cmd(self, root, files, file_folders: list[dict]):
        for file in files:
            file_src = os.path.join(root, file)
            for data_dict in file_folders:
                if file_src == data_dict.get(Cfg.SRC) and os.path.isfile(file_src):
                    self.compress[file_src] = data_dict.get(Cfg.MAX_SIZE_KB)

    def images_in_dir_cmd(self, directory, max_size_kb):
        for root_, _, files_ in os.walk(directory):
            for file_ in files_:
                img_src = os.path.join(root_, file_)
                if os.path.isfile(img_src) and img_src.endswith(Cfg.IMG_EXTS):
                    self.compress[img_src] = max_size_kb

    def remaining_files_cmd(self, base_path):
        for root, dirs, files in os.walk(base_path):
            for name in dirs + files:
                item_path = os.path.join(root, name)
                if item_path not in self.compress and item_path.endswith(Cfg.IMG_EXTS):
                    self.compress[item_path] = 99999

    def get_compress_list(self):
        named_folders = self.data.get(Cfg.NAMED_FOLDERS)
        file_folders = self.data.get(Cfg.SPECIFIC_FOLDERS)
        others = self.data.get(Cfg.OTHERS)

        for root, dirs, files in os.walk(self.base_path):

            if named_folders:
                self.named_folders_cmd(root, dirs, named_folders)

            if file_folders:
                self.specific_folders_cmd(root, dirs, file_folders)
                self.specific_files_cmd(root, files, file_folders)

        if others:
            self.remaining_files_cmd(self.base_path)

        for img_src, max_size_kb in self.compress.items():
            print(img_src, max_size_kb)

# Пример использования
base_path = '/Users/Loshkarev/Desktop/test'

data = {
    Cfg.NAMED_FOLDERS: [
        {'src': 'ХО', 'max_size_kb': 100},
        {'src': 'ГО', 'max_size_kb': 50}
    ],
    # Cfg.SPECIFIC_FOLDERS: [
    #     {'src': '/Users/Loshkarev/Desktop/test/Test 2', 'max_size_kb': 666}, 
    #     {'src': '/Users/Loshkarev/Desktop/test/Test/file 1.jpg', 'max_size_kb': 123}
    # ],
    # Cfg.OTHERS: [
    #     {"src": None, "max_size_kb": 1000}
    # ]
}

prc = FileProcessor(base_path, data)
prc.get_compress_list()