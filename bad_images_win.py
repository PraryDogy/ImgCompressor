import os
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget)


class BadImgWin(QWidget):
    def __init__(self, images: list[tuple]):
        """
        images: (real size, desired size, path)
        """
        super().__init__()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Внимание")
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)
        self.images = images

        desired_size = images[0][1]
        title = QLabel(f"Не удалось достаточно сжать до {desired_size}кб:\n")
        main_lay.addWidget(title)

        for real_size, desired_size, path in images:
            text = path
            limit = 150
            real_size = int(real_size)
            if len(text) > limit:
                text = "..." + text[-limit:]
            text = f"{text} ({real_size}кб)"
            path_label = QLabel(text)
            main_lay.addWidget(path_label)
            path_label.mouseReleaseEvent = lambda e, path=path: self.cmd(path)

        self.resize(300, 300)
        self.adjustSize()

    def cmd(self, path: str):
        subprocess.Popen(["open", "-R", path])

    def center_relative_parent(self, parent: QWidget):

        try:
            geo = self.geometry()
            geo.moveCenter(parent.geometry().center())
            self.setGeometry(geo)
        except (RuntimeError, Exception) as e:
            pass