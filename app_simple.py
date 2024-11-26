import os

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent, QResizeEvent
from PyQt5.QtWidgets import (QFileDialog, QFrame, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QMessageBox, QPushButton, QSpacerItem,
                             QVBoxLayout, QWidget, QApplication)

from cfg import Cfg
from util import CompressThreadBased


class Shared:
    my_app = None



class DynamicWidget(QWidget):
    removed = pyqtSignal()

    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.my_parent = parent

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

        up_wid = QWidget(parent=self)
        v_layout.addWidget(up_wid)

        up_layout = QHBoxLayout()
        up_layout.setContentsMargins(0, 0, 0, 0)
        up_wid.setLayout(up_layout)

        self.browse_btn = QPushButton(parent=self, text="Обзор")
        self.browse_btn.setFixedWidth(100)
        self.browse_btn.clicked.connect(self.browse_btn_cmd)
        up_layout.addWidget(self.browse_btn)

        self.browse_label = QLabel(parent=self, text="Нажмите обзор и выберите папку для сжатия изображений")
        self.browse_label.setWordWrap(True)
        up_layout.addWidget(self.browse_label)

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

    def dragEnterEvent(self, a0: QDragEnterEvent | None) -> None:
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
        return super().dragEnterEvent(a0)
    
    def dragLeaveEvent(self, a0: QDragLeaveEvent | None) -> None:
        return super().dragLeaveEvent(a0)

    def dropEvent(self, a0: QDropEvent | None) -> None:
        path = a0.mimeData().urls()[0].toLocalFile()
        if os.path.isdir(path):
            self.browse_label.setText(path)
            return super().dropEvent(a0)
    
    def browse_btn_cmd(self):
        dest = QFileDialog.getExistingDirectory()

        if dest:
            self.browse_label.setText(dest)

    def get_data(self):
        dest = self.browse_label.text()

        if "Нажмите" in dest:
            return None

        try:
            right_input_value = int(self.input_wid.text().strip())
            right_input_value = right_input_value - 5
        except Exception as e:
            return None

        return {
            "destination": dest,
            "file_size": right_input_value
            }

    def my_sep(self):
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: black;")
        return sep


class AppSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'{Cfg.app_name}: сжатие без условий')

        self.setMinimumSize(560, 400)

        if Cfg.geo:
            self.setGeometry(Cfg.geo)
        else:
            self.resize(560, 400)
            geo = QApplication.primaryScreen().geometry()
            x = geo.width() // 2 - self.width() // 2
            y = geo.height() // 2 - self.height() // 2
            self.move(x, y)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 10, 0, 0)
        self.setLayout(self.v_layout)


        self.mode_btn = QPushButton("Включить сжатие по условиям")
        self.mode_btn.clicked.connect(self.mode_btn_cmd)
        self.v_layout.addWidget(self.mode_btn, alignment=Qt.AlignmentFlag.AlignCenter)




        self.browseTitle = QLabel('Выберите одну или несколько папок')
        self.v_layout.addWidget(self.browseTitle)

        self.add_btn = QPushButton("+ Добавить папку")
        self.add_btn.clicked.connect(self.add_btn_cmd)
        self.add_btn.setFixedWidth(200)
        self.v_layout.addWidget(self.add_btn)




        self.list_widget = QListWidget(parent=self)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.list_widget.verticalScrollBar().setSingleStep(15)
        self.v_layout.addWidget(self.list_widget)

        spacer_item = QListWidgetItem()
        spacer_item.setSizeHint(QSize(0, 10))
        self.list_widget.addItem(spacer_item)

        self.start_btn = QPushButton("Старт")
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start_btn_start_cmd)
        self.v_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.statement_widgets: list[DynamicWidget] = []

    def add_btn_cmd(self):
        list_item = QListWidgetItem()
        wid = DynamicWidget(title="hello", parent=self)
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
                t = "Заполните все данные в условиях.\nУкажите путь к папке, введите целое число"
                self.show_warning(t)
                return


        self.start_btn.setText("Стоп")
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_btn_stop_cmd)

        try:
            self.task = CompressThreadBased(data=data)
            self.switch_widgets(True)
            self.task.finished.connect(self.finished_task)
            self.task.start()
        except Exception as e:
            self.show_warning(f"Обратитесь к разрабочику\nОшибка при запуске QThread\n{e}")

    def finished_task(self):
        self.start_btn.setText("Старт")
        self.switch_widgets(False)
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_btn_start_cmd)

    def start_btn_stop_cmd(self):
        self.start_btn.setText("Старт")
        self.switch_widgets(False)
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
        msg.setGeometry(0, 0, 100, 100)
        msg.adjustSize()

        geo = msg.geometry()
        geo.moveCenter(self.geometry().center())
        msg.setGeometry(geo)

        msg.exec_()

    def mode_btn_cmd(self):
        from app_statement import AppStatement
        self.hide()

        Cfg.geo = self.geometry()
        self.app_ext = AppStatement()
        Shared.my_app = self.app_ext
        self.app_ext.show()

        try:
            self.task.force_cancel.emit()
        except Exception as e:
            pass

        self.deleteLater()

    def switch_widgets(self, disabled: bool):
        for i in (self.mode_btn, self.browseTitle, self.add_btn, self.list_widget):
            try:
                i.setDisabled(disabled)
            except Exception as e:
                print(e)