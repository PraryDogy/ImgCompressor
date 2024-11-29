import os

from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent
from PyQt5.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
                             QListWidget, QListWidgetItem, QMessageBox,
                             QPushButton, QSpacerItem, QVBoxLayout, QWidget)

from win_process import ProcessWin
from cfg import Cfg
from utils import NoStatementTask


class Shared:
    my_app = None



class DynamicWidget(QWidget):
    removed = pyqtSignal()

    def __init__(self, parent: QWidget, path_: str):
        super().__init__(parent=parent)
    
        self.path_ = path_

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

        self.path_lbl = QLabel(text=path_)
        v_layout.addWidget(self.path_lbl)

        input_label = QLabel(parent=self, text=" До какого размера сжать в kb")
        v_layout.addWidget(input_label)

        self.input_wid = QLineEdit(parent=self)
        self.input_wid.setPlaceholderText("Введите целое число")
        self.input_wid.setFixedSize(250, 30)
        v_layout.addWidget(self.input_wid)

        self.input_wid.setStyleSheet("padding-left: 5px; background-color: #3b590d;")
        QTimer.singleShot(500, lambda: self.input_wid.setStyleSheet("padding-left: 5px;"))

        self.remove_btn = QPushButton(parent=self, text="Удалить")
        self.remove_btn.setFixedWidth(200)
        self.remove_btn.clicked.connect(self.remove_btn_cmd)
        v_layout.addWidget(self.remove_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        v_layout.addSpacerItem(QSpacerItem(0, 10))
        v_layout.addWidget(self.my_sep())
        v_layout.addSpacerItem(QSpacerItem(0, 10))

    def remove_btn_cmd(self):
        self.removed.emit()
    
    def get_data(self):
        """place, max_size_kb"""
        place = self.path_

        try:
            right_input_value = int(self.input_wid.text().strip())
            right_input_value = right_input_value - 5
        except Exception as e:
            return None

        return (place, right_input_value)

    def my_sep(self):
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: black;")
        return sep


class WidNoStat(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.main_lay = QVBoxLayout()
        self.main_lay.setContentsMargins(0, 10, 0, 0)
        self.setLayout(self.main_lay)

        t = [
            "Сжатие без условий:",
            "Перетяните файлы или папки и программа",
            "сожмет все изображения внутри этих папок."
        ]

        t = "\n".join(t)

        self.browseTitle = QLabel(t)
        self.main_lay.addWidget(self.browseTitle)

        self.list_widget = QListWidget(parent=self)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.list_widget.verticalScrollBar().setSingleStep(15)
        self.main_lay.addWidget(self.list_widget)

        spacer_item = QListWidgetItem()
        spacer_item.setSizeHint(QSize(0, 10))
        self.list_widget.addItem(spacer_item)

        self.start_btn = QPushButton("Старт")
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start_btn_start_cmd)
        self.main_lay.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.statement_widgets: list[DynamicWidget] = []

    def add_btn_cmd(self, path_: str):
        list_item = QListWidgetItem()

        wid = DynamicWidget(parent=self, path_=path_)
        wid.removed.connect(lambda: self.removed_cmd(list_item, wid))
        list_item.setSizeHint(wid.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, wid)

        self.statement_widgets.append(wid)

    def removed_cmd(self, list_item: QListWidgetItem, wid: DynamicWidget):
        self.statement_widgets.remove(wid)

        item_index = self.list_widget.row(list_item)
        item = self.list_widget.takeItem(item_index)
        self.list_widget.removeItemWidget(item)
        del item

    def start_btn_start_cmd(self):
        if not self.statement_widgets:
            return

        data = []

        for i in self.statement_widgets:
            i_data = i.get_data()

            if i_data:
                data.append(i_data)

            else:
                t = [
                    "Заполните все данные в условиях.",
                    "Укажите путь к папке, введите целое число"
                ]
                t = "\n".join(t)
                self.show_warning(t)
                return

        self.task_ = NoStatementTask(data=data)

        self.win_ = ProcessWin()

        self.win_.stop_.connect(self.task_.stop_cmd)
        self.task_.finished_.connect(self.finished_task)
        self.task_.feedback.connect(lambda data: self.win_.set_labels_cmd(**data))

        self.task_.start()
        self.win_.center_relative_parent(parent=self)
        self.win_.show()

    def finished_task(self):
        self.win_.deleteLater()

    def show_warning(self, text: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Внимание")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setGeometry(0, 0, 100, 100)
        msg.adjustSize()

        geo = msg.geometry()
        geo.moveCenter(self.geometry().center())
        msg.setGeometry(geo)

        msg.exec_()

    def dragEnterEvent(self, a0: QDragEnterEvent | None) -> None:
        self.raise_()
        self.show()

        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
        return super().dragEnterEvent(a0)
    
    def dragLeaveEvent(self, a0: QDragLeaveEvent | None) -> None:
        return super().dragLeaveEvent(a0)

    def dropEvent(self, a0: QDropEvent | None) -> None:
        paths = a0.mimeData().urls()

        for i in paths:
            path_ = i.toLocalFile()

            if os.path.isdir(path_):
                self.add_btn_cmd(path_=path_)
            else:
                self.add_btn_cmd(path_=path_)
