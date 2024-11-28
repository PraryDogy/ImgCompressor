from PyQt5.QtCore import Qt, QThread, pyqtSignal
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
        self.stop_btn.clicked.connect(self.stop_.emit)
        v_lay.addWidget(self.stop_btn)

        self.feedback.connect(lambda data: self.set_labels_cmd(**data))

    def set_labels_cmd(self, current: int, total: int, place: str):
        self.total_label.setText(f"Сжато: {current} из {total}")
        self.place_label.setText(place)

    def center_relative_parent(self, parent: QWidget):

        try:
            geo = self.geometry()
            geo.moveCenter(parent.geometry().center())
            self.setGeometry(geo)
        except (RuntimeError, Exception) as e:
            pass