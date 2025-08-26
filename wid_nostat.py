import os

from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit,
                             QListWidget, QListWidgetItem, QMessageBox,
                             QPushButton, QSpacerItem, QVBoxLayout, QWidget)

from bad_images_win import BadImgWin
from utils import NoStatementTask
from win_process import ProcessWin


class DynamicWidget(QWidget):
    removed = pyqtSignal()

    def __init__(self, parent: QWidget, path_: str):
        super().__init__(parent=parent)
    
        self.path_ = path_

        h_lay = QHBoxLayout()
        h_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h_lay)

        limit = 50
        if len(path_) > limit:
            dest = "..." + path_[-limit:]
        else:
            dest = path_

        self.path_lbl = QLabel(text=dest)
        h_lay.addWidget(self.path_lbl)

        self.input_wid = QLineEdit(parent=self)
        self.input_wid.setStyleSheet("padding-left: 2px; padding-right: 2px;")
        self.input_wid.setPlaceholderText("Введите целое число")
        self.input_wid.setFixedSize(170, 30)
        h_lay.addWidget(self.input_wid)

        self.remove_btn = QPushButton(text="x")
        self.remove_btn.setFixedWidth(40)
        self.remove_btn.clicked.connect(self.removed.emit)
        h_lay.addWidget(self.remove_btn)

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
            "Перетяните папку / файл, укажите размер.",
            "Программа сожмет все изображения внутри этой папки."
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
                    "Укажите размер для сжатия."
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
        self.win_.center_relative_parent(parent=self.window())
        self.win_.show()

    def finished_task(self, bad_images: list[tuple]):
        if bad_images:
            self.bad_img_win = BadImgWin(bad_images)
            self.bad_img_win.center_relative_parent(self.window())
            self.bad_img_win.show()
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
        geo.moveCenter(self.window().geometry().center())
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
