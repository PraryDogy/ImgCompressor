import os

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class ProcessWin(QWidget):
    stop_ = pyqtSignal()
    feedback = pyqtSignal(dict)

    def __init__(self):
        """current, total, place"""

        super().__init__()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        fl = Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint
        fl = fl  | Qt.WindowType.WindowCloseButtonHint
        self.setWindowFlags(fl)
        self.setFixedSize(250, 150)

        v_lay = QVBoxLayout()
        self.setLayout(v_lay)
        
        self.total_label = QLabel(text="Сжато: вычисляю...")
        v_lay.addWidget(self.total_label)

        self.place_label = QLabel(text="")
        v_lay.addWidget(self.place_label)

        self.stop_btn = QPushButton("Стоп")
        self.stop_btn.clicked.connect(self.stop_cmd)
        v_lay.addWidget(self.stop_btn)

        self.feedback.connect(lambda data: self.set_labels_cmd(**data))

    def set_labels_cmd(self, current: int, total: int, place: str):
        try:
            place = os.path.basename(place.strip().strip(os.sep))
            self.total_label.setText(f"Сжато: {current} из {total}")
            self.place_label.setText(f"Папка: {place}")
        except RuntimeError:
            ...

    def center_relative_parent(self, parent: QWidget):

        try:
            geo = self.geometry()
            geo.moveCenter(parent.geometry().center())
            self.setGeometry(geo)
        except (RuntimeError, Exception) as e:
            pass

    def stop_cmd(self, *args):
        self.stop_.emit()
        self.deleteLater()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        a0.ignore()