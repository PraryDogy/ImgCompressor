import os

from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import (QDragEnterEvent, QDragLeaveEvent, QDropEvent,
                         QResizeEvent)
from PyQt5.QtWidgets import (QFileDialog, QFrame, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QMessageBox, QPushButton, QSpacerItem,
                             QVBoxLayout, QWidget)

from utils import StatementTask


class StatWidBase(QWidget):
    removed = pyqtSignal()

    def __init__(self):
        super().__init__()
        ...
        # гор виджет
        # верт верт удалить

        self.main_lay = QHBoxLayout()





class StatWid(QWidget):
    removed = pyqtSignal()

    def __init__(self):
        super().__init__()

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
        self.left_input.setPlaceholderText("Имя папки")
        left_layout.addWidget(self.left_input)

        self.left_input.setStyleSheet("padding-left: 5px; background-color: #3b590d;")
        QTimer.singleShot(500, lambda: self.left_input.setStyleSheet("padding-left: 5px;"))

        right_wid = QWidget(parent=self)
        h_layout.addWidget(right_wid, alignment=Qt.AlignmentFlag.AlignRight)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_wid.setLayout(right_layout)

        right_lbl = QLabel(parent=self, text=f" Уменьшить до kb")
        right_layout.addWidget(right_lbl)

        self.right_input = QLineEdit(parent=self)
        self.right_input.setFixedHeight(30)
        self.right_input.setFixedWidth(200)
        self.right_input.setPlaceholderText("Размер в килобайтах")
        right_layout.addWidget(self.right_input)

        self.right_input.setStyleSheet("padding-left: 5px; background-color: #3b590d;")
        QTimer.singleShot(500, lambda: self.right_input.setStyleSheet("padding-left: 5px;"))


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


class FolderWid(QWidget):
    removed = pyqtSignal()

    def __init__(self, path: str, parent: QWidget = None):
        super().__init__(parent)
        self.path_ = path

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

        left_lbl = QLabel(parent=self, text=f" Сжать ТОЛЬКО в этой папке")
        left_layout.addWidget(left_lbl)

        path = os.sep + path.strip().strip(os.sep)
        self.left_input = QLabel(text=os.path.basename(path))
        self.left_input.setFixedHeight(30)
        left_layout.addWidget(self.left_input)

        right_wid = QWidget(parent=self)
        h_layout.addWidget(right_wid, alignment=Qt.AlignmentFlag.AlignRight)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_wid.setLayout(right_layout)

        right_lbl = QLabel(parent=self, text=f" Уменьшить до kb")
        right_layout.addWidget(right_lbl)

        self.right_input = QLineEdit(parent=self)
        self.right_input.setFixedHeight(30)
        self.right_input.setFixedWidth(200)
        self.right_input.setPlaceholderText("Размер в килобайтах")
        right_layout.addWidget(self.right_input)

        self.right_input.setStyleSheet("padding-left: 5px; background-color: #3b590d;")
        QTimer.singleShot(500, lambda: self.right_input.setStyleSheet("padding-left: 5px;"))

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
        try:
            right_input_value = int(self.right_input.text().strip())
            # вычитаем 5кб от заданного размера на всякий случай
            right_input_value = right_input_value - 5
        except Exception as e:
            return None
        
        left_input_value = self.path_.strip()
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


class WidStat(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.main_folder = None
        self.stat_wids: list[StatWid | FolderWid] = []

        self.main_lay = QVBoxLayout()
        self.main_lay.setContentsMargins(0, 10, 0, 0)
        self.setLayout(self.main_lay)


        self.browse_wid = QWidget()
        self.browse_wid.setFixedHeight(50)
        self.main_lay.addWidget(self.browse_wid)

        browse_lay = QHBoxLayout()
        browse_lay.setContentsMargins(0, 0, 0, 0)
        self.browse_wid.setLayout(browse_lay)

        self.browse_btn = QPushButton("Главная папка")
        self.browse_btn.clicked.connect(self.browse_main_folder)
        self.browse_btn.setFixedWidth(200)
        browse_lay.addWidget(self.browse_btn)


        self.main_folder_lbl = QLabel('Можно перетянуть сюда главную папку')
        browse_lay.addWidget(self.main_folder_lbl)

        t = [
            "Описание условий",
            "",
            "Условие:",
            "Папка с именем *** внутри главной папки будет сжата до *** кб",
            "",
            "Файл/папка:",
            "Указанный файл/папка внутри главной папки будут сжаты до *** кб",
            "",
            "Остальное:",
            "Все остальные файлы внутри главной папки будут сжаты до *** кб",
        ]
        t = "\n".join(t)
        self.description = QLabel(t)
        self.main_lay.addWidget(self.description)


        self.btns_wid = QWidget()
        self.main_lay.addWidget(self.btns_wid)

        btns_lay = QHBoxLayout()
        btns_lay.setContentsMargins(0, 0, 0, 0)
        self.btns_wid.setLayout(btns_lay)

        self.add_btn = QPushButton("Условие")
        self.add_btn.clicked.connect(lambda: self.add_stat_wid(flag="stat"))
        self.add_btn.setFixedWidth(150)
        btns_lay.addWidget(self.add_btn)

        self.add_btn_two = QPushButton("Папка/файл")
        self.add_btn_two.clicked.connect(lambda: self.add_stat_wid(flag="folder"))
        self.add_btn_two.setFixedWidth(150)
        btns_lay.addWidget(self.add_btn_two)
        
        self.add_btn_two = QPushButton("Остальное")
        self.add_btn_two.clicked.connect(lambda: self.add_stat_wid(flag="other"))
        self.add_btn_two.setFixedWidth(150)
        btns_lay.addWidget(self.add_btn_two)

        btns_lay.addStretch()


        self.list_widget = QListWidget(parent=self)
        self.list_widget.verticalScrollBar().setSingleStep(15)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.main_lay.addWidget(self.list_widget)

        spacer_item = QListWidgetItem()
        spacer_item.setSizeHint(QSize(0, 10))
        self.list_widget.addItem(spacer_item)

        self.start_btn = QPushButton("Старт")
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start_btn_cmd)
        self.main_lay.addWidget(
            self.start_btn,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # иначе фокус по умолчанию почему то на кнопке "главная папка"
        QTimer.singleShot(200, self.setFocus)

    def browse_main_folder(self):
        dest = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if dest:
            self.main_folder_lbl.setWordWrap(True)
            self.main_folder_lbl.setText(dest)
            self.main_folder = dest

    def add_stat_wid(self, flag: str, dest: str = None):

        if not self.main_folder:
            self.show_warning("Укажите главную папку")
            return

        if flag == "stat":
            wid = StatWid()

        elif flag == "folder":

            if dest is None:
                dest = QFileDialog.getExistingDirectory(self)

            if dest:
                wid = FolderWid(path=dest, parent=self)
            else:
                return
            
        elif flag == "other":
            ...

        list_item = QListWidgetItem()
        cmd_ = lambda: self.stat_wid_removed_cmd(list_item, wid)
        wid.removed.connect(cmd_)
        list_item.setSizeHint(wid.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, wid)
        self.stat_wids.append(wid)

    def stat_wid_removed_cmd(self, list_item: QListWidgetItem, wid: StatWid):
        self.stat_wids.remove(wid)
        item_index = self.list_widget.row(list_item)
        item = self.list_widget.takeItem(item_index)
        self.list_widget.removeItemWidget(item)
        del item

    def start_btn_cmd(self):

        if not self.stat_wids:
            self.show_warning("Добавьте условия")
            return

        if not self.main_folder:
            self.show_warning("Укажите папку")
            return

        data = []

        for i in self.stat_wids:
            i_data = i.get_data()

            if i_data:
                data.append(i_data)
            else:
                t = [
                    "Заполните все данные в условиях",
                    "Слева имя папки, справа целое число"
                ]
                t = "\n".join(t)
                self.show_warning(t)
                return
            
        print(data)
        return

        try:
            self.task = StatementTask(root_dir=self.main_folder, data=data)
            # self.task.finished.connect(self.finished_task)
            self.task.start()
        except Exception as e:
            self.show_warning(f"Обратитесь к разрабочику\nОшибка при запуске QThread\n{e}")

    def show_warning(self, text: str):

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.adjustSize()

        geo = msg.geometry()
        geo.moveCenter(self.window().geometry().center())
        msg.setGeometry(geo)

        msg.exec_()

    def dragEnterEvent(self, a0: QDragEnterEvent | None) -> None:

        self.raise_()
        self.show()
        self.setFocus()

        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
        return super().dragEnterEvent(a0)
    
    def dragLeaveEvent(self, a0: QDragLeaveEvent | None) -> None:
        return super().dragLeaveEvent(a0)

    def dropEvent(self, a0: QDropEvent | None) -> None:
        screen_height = self.height()
        drop_position = a0.pos().y()
        paths = a0.mimeData().urls()

        if not paths:
            return

        if drop_position < screen_height / 2:
            # если это в верхней половине экрана
            
            path_ = paths[0].toLocalFile()
            path_ = path_ if os.path.isdir(path_) else None

            if path_:
                self.main_folder_lbl.setWordWrap(True)
                self.main_folder_lbl.setText(path_)
                self.main_folder = path_

        else:
            # если в нижней части экрана

            for path_ in paths:

                path_ = path_.toLocalFile()

                if not self.main_folder:
                    self.show_warning("Сначала укажите главную папку")
                    break

                if self.main_folder in path_ and self.main_folder != path_:
                    self.add_stat_wid(flag="folder", dest=path_)

                else:
                    self.show_warning("Файл/папка должны быть в главной папке")

        super().dropEvent(a0)
