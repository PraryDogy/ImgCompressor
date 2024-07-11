import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QFileDialog, QFrame, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QPushButton,
                             QScrollArea, QSpacerItem, QVBoxLayout, QWidget)

from util import CompressThread


class DynamicWidget(QWidget):
    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.my_parent = parent

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h_layout)

        left_wid = QWidget()
        h_layout.addWidget(left_wid)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_wid.setLayout(left_layout)

        left_lbl = QLabel(f" Если имя папки как указано ниже")
        left_layout.addWidget(left_lbl)

        self.left_input = QLineEdit()
        self.left_input.setFixedHeight(30)
        self.left_input.setPlaceholderText("Напишите имя папки")
        left_layout.addWidget(self.left_input)

        right_wid = QWidget()
        h_layout.addWidget(right_wid)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_wid.setLayout(right_layout)

        right_lbl = QLabel(f" Уменьшить до kb")
        right_layout.addWidget(right_lbl)

        self.right_input = QLineEdit()
        self.right_input.setFixedHeight(30)
        self.right_input.setPlaceholderText("Напишите размер в килобайтах")
        right_layout.addWidget(self.right_input)

    def get_data(self):
        try:
            right_input_value = int(self.right_input.text().strip())
        except ValueError as e:
            return None
        
        left_input_value = self.left_input.text().strip()
        if not left_input_value:
            return None

        return {
            "folder_name": left_input_value,
            "file_size": right_input_value
            }


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.my_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Compressor')
        self.setMinimumSize(560, 400)
        self.setGeometry(100, 100, 560, 400)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 10, 0, 0)
        self.setLayout(self.v_layout)

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




        scroll_area = QScrollArea()
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidgetResizable(True)
        self.v_layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
    
        self.scroll_v_layout = QVBoxLayout()
        self.scroll_v_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self.scroll_v_layout)

        self.scroll_v_layout.insertStretch(-1, 10)

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

    def my_sep(self):
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: black")
        return sep

    def add_btn_cmd(self):
        wid = DynamicWidget(title="hello", parent=self)
        self.statement_widgets.append(wid)
        self.scroll_v_layout.insertWidget(0, wid)

        remove_btn = QPushButton("Удалить")
        remove_btn.setFixedWidth(200)
        self.scroll_v_layout.insertWidget(1, remove_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        sep = self.my_sep()
        self.scroll_v_layout.insertWidget(2, sep)

        remove_btn.clicked.connect(lambda: self.remove_btn_cmd([wid, remove_btn, sep]))

    def remove_btn_cmd(self, widgets: list[QWidget]):
        self.statement_widgets.remove(widgets[0])
        for i in widgets:
            i.deleteLater()

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
