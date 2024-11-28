from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class ProcessWin(QWidget):
    stop_ = pyqtSignal()
    set_labels = pyqtSignal(dict)

    def __init__(self):
        """current, total, place"""

        super().__init__()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        v_lay = QVBoxLayout()
        self.setLayout(v_lay)
        
        self.total_label = QLabel(text="Сжато: вычисляю...")
        v_lay.addWidget(self.total_label)

        self.place_label = QLabel(text="")
        v_lay.addWidget(self.place_label)

        self.stop_btn = QPushButton("Стоп")
        self.stop_btn.clicked.connect(self.stop_.emit)
        v_lay.addWidget(self.stop_btn)

        self.set_labels.connect(self.set_labels_cmd)

    def set_labels_cmd(self, current: int, total: int, place: str):
        self.total_label.setText(f"Сжато: {current} из {total}")
        self.place_label.setText(place)