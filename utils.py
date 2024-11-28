import os

from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


IMG_EXTS = ('.jpg', '.jpeg', '.png')


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

                    if file.endswith(IMG_EXTS):
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

                if file.endswith(IMG_EXTS):
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

    def __init__(self, root_dir: str, data: dict):
        """
        [ {"folder_name": str, "file_size": int}, ... ]
        """

        super().__init__()
        self.force_cancel.connect(self.stop_cmd)
        self.root_dir = root_dir
        self.data = data

        self.can_run = True

    def run(self):
        Shared.flag = True
        self.process_images(root_dir=self.root_dir, data=self.data)
        self.finished.emit()

    def stop_cmd(self):
        Shared.flag = False

    def process_images(self, root_dir: str, data: list[dict]):
        """
        [ {"folder_name": str, "file_size": int}, ... ]
        """

        named_folders: list[dict] = []
        single_folders: list[dict] = []
        files_: list[dict] = []

        for i in data:

            if os.path.isdir(i.get("folder_name")):
                single_folders.append(i)

            elif os.path.isfile(i.get("folder_name")):
                files_.append(i)

            else:
                named_folders.append(i)

        # делаем ресайзы в конкретных папках
        for dict_ in single_folders:

            if not self.can_run:
                return

            self.walk_folder(
                dict_.get("folder_name"),
                dict_.get("file_size")
                )
            
        # делаем ресайзы в конкретных папках
        for dict_ in files_:

            if not self.can_run:
                return

            Utils.resize_image(
                dict_.get("folder_name"),
                dict_.get("file_size")
                )

        # делаем ресайзы в папках с именами
        # for root, _, files in os.walk(root_dir):

        #     for filename in files:

        #         if not self.can_run:
        #             return

        #         if filename.lower().endswith(IMG_EXTS):

        #             image_path = os.path.join(root, filename)

        #             for data_dict in folder_names:
        #                 folder_name = data_dict.get("folder_name")

        #                 if os.sep + folder_name + os.sep in image_path:
        #                     if not self.can_run:

        #                         Utils.resize_image(
        #                             image_path=image_path,
        #                             max_size_kb=data_dict["file_size"]
        #                         )

    def walk_folder(self, folder_path, max_size_kb: int):

        for root, dirs, files in os.walk(folder_path):

            if not Shared.flag:
                return

            for file in files:

                if not Shared.flag:
                    return

                src: str = os.path.join(root, file)

                if src.lower().endswith(IMG_EXTS):
                    Utils.resize_image(src, max_size_kb)