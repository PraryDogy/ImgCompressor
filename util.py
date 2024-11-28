import os

from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


IMG_EXTS = ('.jpg', '.jpeg', '.png')


class Utils:

    @classmethod
    def resize_image(cls, img_src: str, max_size: int):
        current_size_kb = int(os.path.getsize(img_src) // 1024.0)

        if current_size_kb <= max_size:
            return

        img = Image.open(img_src)
        quality = 95

        while True:
            img.save(img_src, optimize=True, quality=quality)
            if os.path.getsize(img_src) <= max_size * 1024 or quality <= 10:
                break
            quality -= 5


class ComprerssNoState(QThread):
    can_run = True
    finished_ = pyqtSignal()
    feedback = pyqtSignal(dict)

    def __init__(self, data: tuple[tuple[str, int]]):
        super().__init__()
        self.data = data

        "current, total, place > app_win_process"
        self.current: int = 0
        self.total: int = 0

    def run(self):
        self.get_total()

        for single_data in self.data:

            if not self.can_run:
                return

            path, max_size_kb = single_data
            self.walk_dir(
                path=path,
                max_size_kb=max_size_kb
            )

        self.finished_.emit()

    def get_total(self):

        for single_data in self.data:

            path, max_size_kb = single_data

            if not self.can_run:
                return

            for root, dirs, files in os.walk(path):
                for file in files:

                    if not self.can_run:
                        return

                    if file.endswith(IMG_EXTS):
                        self.total += 1

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
                        continue

                    "total, current, place > app_win_process"
                    self.current += 1
                    data_ = {
                        "total": self.total,
                        "current": self.current,
                        "place": root
                    }
                    self.feedback.emit(data_)



class Shared:
    flag = True

class CompressUtils:

    @staticmethod
    def resize_image(image_path: str, max_size_kb: int):
        try:
            current_size_kb = int(os.path.getsize(image_path) // 1024.0)

            if current_size_kb <= max_size_kb:
                return

            img = Image.open(image_path)
            quality = 95

            while True:
                img.save(image_path, optimize=True, quality=quality)
                if os.path.getsize(image_path) <= max_size_kb * 1024 or quality <= 10:
                    break
                quality -= 5
        except Exception:
            ...

    @staticmethod
    def resize_folder_folders(folder_path, max_size_kb: int):
        for root, dirs, files in os.walk(folder_path):
            if not Shared.flag:
                return
            for file in files:
                if not Shared.flag:
                    return
                src: str = os.path.join(root, file)
                if src.lower().endswith(('.jpg', '.jpeg', '.png')):
                    CompressUtils.resize_image(src, max_size_kb)


class CompressThread(QThread):
    finished_ = pyqtSignal()
    force_cancel = pyqtSignal()

    def __init__(self, root_dir: str, data: dict):
        """
        [ {"folder_name": str, "file_size": int}, ... ]
        """

        super().__init__()
        self.force_cancel.connect(self.force_cancel_cmd)
        self.root_dir = root_dir
        self.data = data

    def run(self):
        Shared.flag = True
        self.process_images(root_dir=self.root_dir, data=self.data)
        self.finished.emit()

    def force_cancel_cmd(self):
        Shared.flag = False

    def process_images(self, root_dir: str, data: list[dict]):
        """
        [ {"folder_name": str, "file_size": int}, ... ]
        """

        folder_names: list[dict] = []
        folder_folders: list[dict] = []

        for i in data:
            if os.path.isdir(i.get("folder_name")):
                folder_folders.append(i)
            else:
                folder_names.append(i)

        # делаем ресайзы в конкретных папках

        for dict_ in folder_folders:
            CompressUtils.resize_folder_folders(
                dict_.get("folder_name"),
                dict_.get("file_size")
                )

        # делаем ресайзы в папках с именами
        for root, _, files in os.walk(root_dir):

            for filename in files:

                if not Shared.flag:
                    return

                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

                    image_path = os.path.join(root, filename)

                    for data_dict in folder_names:
                        folder_name = data_dict.get("folder_name")

                        if os.sep + folder_name + os.sep in image_path:
                            CompressUtils.resize_image(image_path=image_path, max_size_kb=data_dict["file_size"])



class CompressThreadBased(QThread):
    finished = pyqtSignal()
    force_cancel = pyqtSignal()

    def __init__(self, data: dict):
        """
        [ {"destination": str, "file_size": int}, ... ]
        """

        super().__init__()
        self.force_cancel.connect(self.force_cancel_cmd)
        self.data = data

    def run(self):
        Shared.flag = True
        self.process_images(data=self.data)
        self.finished.emit()

    def force_cancel_cmd(self):
        Shared.flag = False

    def process_images(self, data: list[dict]):
        """
        [ {"destination": str, "file_size": int}, ... ]
        """

        for data_dict in data:
            for root, _, files in os.walk(data_dict["destination"]):

                for filename in files:

                    if not Shared.flag:
                        return
                    
                    filename: str

                    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

                        image_path = os.path.join(root, filename)
                        try:
                            CompressUtils.resize_image(image_path=image_path, max_size_kb=data_dict["file_size"])
                        except Exception as e:
                            print(e)