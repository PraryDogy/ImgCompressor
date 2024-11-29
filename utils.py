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


class StatementTask(QThread):
    finished_ = pyqtSignal()
    force_cancel = pyqtSignal()

    def __init__(self, main_folder: str, data: dict[list[dict]]):
        super().__init__()

        self.force_cancel.connect(self.stop_cmd)

        self.main_folder = main_folder
        self.data = data
        self.can_run = True

    def run(self):
        self.process_images()
        self.finished.emit()

    def stop_cmd(self):
        self.can_run = False

    def process_images(self):
        ... 

        # давай сначала найдем все изображения которые надо сжать и заодно
        # это будет тотал изображений


        # [ {"NAMED_FOLDER"}]

        named_folders = self.data.get(Cfg.NAMED_FOLDER)

