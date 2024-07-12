import os
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent, QMouseEvent
from PyQt5.QtWidgets import (QFileDialog, QFrame, QHBoxLayout, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget, QSpacerItem, QListWidget, QListWidgetItem)

from util import CompressThread
from cfg import Cfg

class Shared:
    my_app = None


class DynamicWidget(QWidget):
    removed = pyqtSignal()

    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.my_parent = parent

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

        h_wid = QWidget(parent=self)
        v_layout.addWidget(h_wid)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_wid.setLayout(h_layout)

        left_wid = QWidget(parent=self)
        h_layout.addWidget(left_wid)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_wid.setLayout(left_layout)

        left_lbl = QLabel(parent=self, text=f" Если имя папки РАВНОЗНАЧНО")
        left_layout.addWidget(left_lbl)

        self.left_input = QLineEdit(parent=self)
        self.left_input.setFixedHeight(30)
        self.left_input.setPlaceholderText("Напишите имя папки")
        self.left_input.setStyleSheet("padding-left: 5px;")
        left_layout.addWidget(self.left_input)

        right_wid = QWidget(parent=self)
        h_layout.addWidget(right_wid)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_wid.setLayout(right_layout)

        right_lbl = QLabel(parent=self, text=f" Уменьшить до kb")
        right_layout.addWidget(right_lbl)

        self.right_input = QLineEdit(parent=self)
        self.right_input.setFixedHeight(30)
        self.right_input.setPlaceholderText("Напишите размер в килобайтах")
        self.right_input.setStyleSheet("padding-left: 5px;")
        right_layout.addWidget(self.right_input)

        self.remove_btn = QPushButton(parent=self, text="Удалить")
        self.remove_btn.setFixedWidth(200)
        self.remove_btn.clicked.connect(self.remove_btn_cmd)
        v_layout.addWidget(self.remove_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        v_layout.addSpacerItem(QSpacerItem(0, 10))
        v_layout.addWidget(self.my_sep())
        v_layout.addSpacerItem(QSpacerItem(0, 10))

    def remove_btn_cmd(self):
        self.removed.emit()
        self.deleteLater()

    def get_data(self):
        try:
            right_input_value = int(self.right_input.text().strip())
            right_input_value = right_input_value - 5
        except Exception as e:
            return None
        
        left_input_value = self.left_input.text().strip()
        if not left_input_value:
            return None

        return {
            "folder_name": left_input_value,
            "file_size": right_input_value
            }

    def my_sep(self):
        sep = QFrame(parent=self)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: black;")
        return sep


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.my_path = None
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle(f'{Cfg.app_name}: сжатие по условиям')
        self.setMinimumSize(560, 400)
        self.resize(560, 400)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 10, 0, 0)
        self.setLayout(self.v_layout)


        self.mode_btn = QPushButton("Включить сжатие без условий")
        self.mode_btn.clicked.connect(self.mode_btn_cmd)
        self.v_layout.addWidget(self.mode_btn, alignment=Qt.AlignmentFlag.AlignCenter)




        self.browseTitle = QLabel('Выбранная папка:')
        self.v_layout.addWidget(self.browseTitle)




        h_wid = QWidget()
        h_wid.setFixedHeight(50)
        self.v_layout.addWidget(h_wid)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_wid.setLayout(h_layout)

        self.browse_btn = QPushButton('Обзор')
        self.browse_btn.clicked.connect(self.browse_folder)
        self.browse_btn.setFixedWidth(200)
        h_layout.addWidget(self.browse_btn)

        self.browse_label_path = QLabel('Нажмите обзор и выберите папку')
        h_layout.addWidget(self.browse_label_path)




        h_wid_ = QWidget()
        h_wid_.setFixedHeight(50)
        self.v_layout.addWidget(h_wid_)

        h_layout_ = QHBoxLayout()
        h_layout_.setContentsMargins(0, 0, 0, 0)
        h_wid_.setLayout(h_layout_)

        self.add_btn = QPushButton("+ Добавить условие")
        self.add_btn.clicked.connect(self.add_btn_cmd)
        self.add_btn.setFixedWidth(200)
        h_layout_.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.list_widget = QListWidget(parent=self)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.v_layout.addWidget(self.list_widget)

        self.start_btn = QPushButton("Старт")
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start_btn_start_cmd)
        self.v_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.statement_widgets: list[DynamicWidget] = []

    def browse_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:
            self.browse_label_path.setWordWrap(True)
            self.browse_label_path.setText(directory)
            self.my_path = directory

    def add_btn_cmd(self):
        list_item = QListWidgetItem()
        wid = DynamicWidget(title="hello", parent=self)
        list_item.setSizeHint(wid.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, wid)

        self.statement_widgets.append(wid)

    def start_btn_start_cmd(self):
        if not self.statement_widgets:
            return

        if not self.my_path:
            self.show_warning("Укажите папку")
            return

        data = []

        for i in self.statement_widgets:
            i_data = i.get_data()

            if i_data:
                data.append(i_data)
            else:
                t = "Заполните все данные в условиях.\nСлева имя папки, справа целое число"
                self.show_warning(t)
                return

        self.start_btn.setText("Стоп")
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_btn_stop_cmd)

        try:
            self.task = CompressThread(root_dir=self.my_path, data=data)
            self.task.finished.connect(self.finished_task)
            self.task.start()
        except Exception as e:
            self.show_warning(f"Обратитесь к разрабочику\nОшибка при запуске QThread\n{e}")

    def finished_task(self):
        self.start_btn.setText("Старт")
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_btn_start_cmd)

    def start_btn_stop_cmd(self):
        self.start_btn.setText("Старт")
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_btn_start_cmd)

        try:
            self.task.force_cancel.emit()
        except Exception as e:
            pass

    def show_warning(self, text: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Внимание")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.adjustSize()

        geo = msg.geometry()
        geo.moveCenter(self.geometry().center())
        msg.setGeometry(geo)

        msg.exec_()

    def mode_btn_cmd(self):
        from gui_ext import MyAppExt
        self.hide()

        self.app_ext = MyAppExt()
        Shared.my_app = self.app_ext
        self.app_ext.show()

        try:
            self.task.force_cancel.emit()
        except Exception as e:
            print(e)

        self.deleteLater()

    def dragEnterEvent(self, a0: QDragEnterEvent | None) -> None:
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
        return super().dragEnterEvent(a0)
    
    def dragLeaveEvent(self, a0: QDragLeaveEvent | None) -> None:
        return super().dragLeaveEvent(a0)

    def dropEvent(self, a0: QDropEvent | None) -> None:
        path = a0.mimeData().urls()[0].toLocalFile()
        if os.path.isdir(path):
            self.browse_label_path.setWordWrap(True)
            self.browse_label_path.setText(path)
            self.my_path = path
            return super().dropEvent(a0)