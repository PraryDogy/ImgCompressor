import os
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal


class Shared:
    flag = True


def resize_image(image_path, max_size_kb):
    current_size_kb = os.path.getsize(image_path) / 1024.0
    if current_size_kb <= max_size_kb:
        return None

    img = Image.open(image_path)
    quality = 95
    dir_name, base_name = os.path.split(image_path)
    name, ext = os.path.splitext(base_name)
    temp_path = os.path.join(dir_name, f"{name}_2{ext}")

    while True:
        img.save(temp_path, optimize=True, quality=quality)
        if os.path.getsize(temp_path) <= max_size_kb * 1024 or quality <= 10:
            os.replace(temp_path, image_path)
            break
        quality -= 5

    img.save(image_path, optimize=True, quality=quality)

def process_images(root_dir: str, data: list[dict]):
    """
    [ {"folder_name": str, "file_size": int}, ... ]
    """

    for dirpath, _, filenames in os.walk(root_dir):

        for filename in filenames:

            if not Shared.flag:
                return

            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

                image_path = os.path.join(dirpath, filename)

                for data_dict in data:
                    if os.sep + data_dict["folder_name"] + os.sep in image_path:

                        try:
                            resize_image(image_path, data_dict["file_size"])
                        except Exception as e:
                            print(e)
                            continue

                        continue


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
        process_images(root_dir=self.root_dir, data=self.data)
        self.finished.emit()

    def force_cancel_cmd(self):
        Shared.flag = False