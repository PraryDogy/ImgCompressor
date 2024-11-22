import os

from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal


class Shared:
    flag = True


class CompressUtils:

    @staticmethod
    def resize_image(image_path: str, max_size_kb: int):
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

    @staticmethod
    def resize_folder_folders(folder_path, max_size_kb: int):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                src: str = os.path.join(root, file)
                if src.lower().endswith(('.jpg', '.jpeg', '.png')):
                    CompressUtils.resize_image(src, max_size_kb)


class CompressThread(QThread):
    finished = pyqtSignal()
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