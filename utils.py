import os

from PIL import Image
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from cfg import Cfg


class Shared:
    flag = True


class Utils:

    @classmethod
    def resize_image(cls, img_src: str, max_size: int):
        current_size_kb = int(os.path.getsize(img_src) // 1024.0)

        if current_size_kb <= max_size:
            return

        try:
            img = Image.open(img_src)
            quality = 95

            while True:
                img.save(img_src, optimize=True, quality=quality)
                if os.path.getsize(img_src) <= max_size * 1024 or quality <= 10:
                    break
                quality -= 5
        except Exception:
            pass


class NoStatementTask(QThread):
    finished_ = pyqtSignal()
    feedback = pyqtSignal(dict)

    def __init__(self, data: list[tuple[str, int]]):
        """[ (place, max_size_kb) ]"""
        super().__init__()

        self.data = data
        self.can_run = True

        "current, total, place > app_win_process"
        self.current: int = 0
        self.total: int = 0

    def stop_cmd(self, *args):
        self.can_run = False

    def run(self):
        self.get_total()

        for single_data in self.data:

            if not self.can_run:
                return

            path, max_size_kb = single_data

            if os.path.isdir(path):
                self.walk_dir(
                    path=path,
                    max_size_kb=max_size_kb
                )
            else:
                self.compress_img(img_src=path, max_size_kb=max_size_kb)

        self.finished_.emit()

    def get_total(self):

        for single_data in self.data:

            path, max_size_kb = single_data

            if not self.can_run:
                return
            
            if os.path.isfile(path):
                self.total += 1
                continue

            for root, dirs, files in os.walk(path):
                for file in files:

                    if not self.can_run:
                        return

                    if file.endswith(Cfg.IMG_EXTS):
                        self.total += 1

    def compress_img(self, img_src: str, max_size_kb: int):
        try:
            Utils.resize_image(
                img_src=img_src,
                max_size=max_size_kb
            )

        except Exception as e:
            ...

        "total, current, place > app_win_process"
        self.current += 1
        data_ = {
            "total": self.total,
            "current": self.current,
            "place": os.path.basename(img_src.strip().strip(os.sep))
        }
        self.feedback.emit(data_)

    def walk_dir(self, path: str, max_size_kb: int):

        for root, dirs, files in os.walk(path):

            for file in files:

                if not self.can_run:
                    return

                if file.endswith(Cfg.IMG_EXTS):
                    img_src = os.path.join(root, file)
                    try:
                        Utils.resize_image(
                            img_src=img_src,
                            max_size=max_size_kb
                        )

                    except Exception as e:
                        ...

                    "total, current, place > app_win_process"
                    self.current += 1
                    data_ = {
                        "total": self.total,
                        "current": self.current,
                        "place": root
                    }
                    self.feedback.emit(data_)


class FileProcessor:
    def __init__(self, base_path: str, data: dict):
        self.compress = {}
        self.data = data
        self.base_path = base_path
        self.can_run = True

    def stop_cmd(self):
        self.can_run = False

    def named_folders_cmd(self, root, dirs, named_folders: list[dict]):
        for dir in dirs:
            for data_dict in named_folders:
                if not self.can_run:
                    return
                if dir == data_dict.get(Cfg.SRC):
                    dir_src = os.path.join(root, dir)
                    self.images_in_dir_cmd(dir_src, data_dict.get(Cfg.MAX_SIZE_KB))

    def specific_folders_cmd(self, root, dirs, file_folders: list[dict]):
        for dir in dirs:
            for data_dict in file_folders:
                if not self.can_run:
                    return
                dir_src = os.path.join(root, dir)
                if dir_src == data_dict.get(Cfg.SRC):
                    self.images_in_dir_cmd(dir_src, data_dict.get(Cfg.MAX_SIZE_KB))

    def specific_files_cmd(self, root, files, file_folders: list[dict]):
        for file in files:
            file_src = os.path.join(root, file)
            for data_dict in file_folders:
                if not self.can_run:
                    return
                if file_src == data_dict.get(Cfg.SRC) and os.path.isfile(file_src):
                    self.compress[file_src] = data_dict.get(Cfg.MAX_SIZE_KB)

    def images_in_dir_cmd(self, directory, max_size_kb):
        for root_, _, files_ in os.walk(directory):
            for file_ in files_:
                if not self.can_run:
                    return
                img_src = os.path.join(root_, file_)
                if os.path.isfile(img_src) and img_src.endswith(Cfg.IMG_EXTS):
                    self.compress[img_src] = max_size_kb

    def remaining_files_cmd(self, base_path, others: dict[list]):

        others: dict = others[0]

        for root, dirs, files in os.walk(base_path):
            for name in dirs + files:
                if not self.can_run:
                    return
                item_path = os.path.join(root, name)
                if item_path not in self.compress and item_path.endswith(Cfg.IMG_EXTS):
                    self.compress[item_path] = others.get(Cfg.MAX_SIZE_KB)

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
            self.remaining_files_cmd(self.base_path, others)

        return self.compress
    

class StatementTask(QThread):
    finished_ = pyqtSignal()
    feedback = pyqtSignal(dict)

    def __init__(self, main_folder: str, data: dict[list[dict]]):
        super().__init__()

        self.main_folder = main_folder
        self.data = data
        self.can_run = True

    def run(self):
        self.compressor = FileProcessor(base_path=self.main_folder, data=self.data)
        self.compress_list: dict[str, int] = self.compressor.get_compress_list()

        self.total_ = len(self.compress_list)
        
        self.compress_images()
        self.finished_.emit()

    def compress_images(self):

        for x, (img_src, max_size_kb) in enumerate(self.compress_list.items(), start=1):

            try:

                Utils.resize_image(img_src, max_size_kb)

                data_ = {
                    "total": self.total_,
                    "current": x,
                    "place": img_src
                }
                self.feedback.emit(data_)

                from time import sleep
                sleep(1)

            except Exception as e:
                print("utils compress error", e)
                continue

    def stop_cmd(self):
        self.compressor.stop_cmd()
        self.can_run = False
