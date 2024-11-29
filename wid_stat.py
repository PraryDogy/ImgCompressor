import os
from collections import defaultdict

from PyQt5.QtCore import QEvent, QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import (QDragEnterEvent, QDragLeaveEvent, QDropEvent,
                         QFontMetrics, QMouseEvent, QPainter, QPaintEvent,
                         QWheelEvent)
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QMessageBox, QPushButton, QSlider, QVBoxLayout,
                             QWidget)

from cfg import Cfg
from utils import StatementTask


class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("padding-left: 2px; padding-right: 2px;")


class MyLabel(QLabel):
    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)

        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(
            self.text(),
            Qt.TextElideMode.ElideNone,
            self.width()
        )

        painter.drawText(self.rect(), self.alignment(), elided)
        return super().paintEvent(a0)
    

class StatWid(QWidget):
    removed = pyqtSignal()

    def __init__(self, flag: str, dest: str = None):
        super().__init__()
        self.flag = flag
        self.dest = None

        self.main_lay = QHBoxLayout()
        self.main_lay.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_lay)

        if flag == Cfg.FILE_FOLDER and dest:

            self.dest = dest

            limit = 50
            if len(dest) > limit:
                dest = "..." + dest[:limit]

            self.left_wid = QLabel(text=dest)

        elif flag == Cfg.NAMED_FOLDER:
            
            self.left_wid = CustomLineEdit()
            self.left_wid.setFixedHeight(30)
            self.left_wid.setPlaceholderText("Папка с именем ***")

        elif flag == Cfg.MAIN_FOLDER:

            self.left_wid = QLabel(text="Остальное")


        self.main_lay.addWidget(self.left_wid)

        self.right_wid = CustomLineEdit()
        self.right_wid.setFixedHeight(30)
        self.right_wid.setFixedWidth(200)
        self.right_wid.setPlaceholderText("Размер в килобайтах")
        self.main_lay.addWidget(self.right_wid)

        self.remove_btn = QPushButton(text="x")
        self.remove_btn.setFixedWidth(40)
        self.remove_btn.clicked.connect(self.removed.emit)
        self.main_lay.addWidget(self.remove_btn)

    def get_data(self):
        """
        returns
        `Cfg.WID_SRC_KEY`, `Cfg.WID_SIZE_KEY`
        """

        max_size_kb = self.right_wid.text().strip()

        try:
            max_size_kb = int(
                self.right_wid.text().strip()
            )
        except Exception:
            return None
        
        if self.flag == Cfg.NAMED_FOLDER:
            src = os.sep + self.left_wid.text().strip()

        elif self.flag == Cfg.FILE_FOLDER:
            src = os.sep + self.dest.strip().strip(os.sep)

        # извлекаем инфу слева у нас там либо окно ввода для named folder
        # либо конкретная папка
        # либо это все остальные файлы

        return {
            Cfg.FLAG: self.flag,
            Cfg.SRC: src,
            Cfg.MAX_SIZE_KB: max_size_kb - 5
            }


class WidStat(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.main_folder = None
        self.stat_wids: list[StatWid] = []

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
            "Все папки с именем *** внутри главной папки будут сжаты до *** кб",
            "",
            "Папка / файл:",
            "Указанные папка / файл внутри главной папки будут сжаты до *** кб",
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
        self.add_btn.clicked.connect(lambda: self.add_stat_wid(flag=Cfg.NAMED_FOLDER))
        self.add_btn.setFixedWidth(150)
        btns_lay.addWidget(self.add_btn)

        self.add_btn_two = QPushButton("Папка / файл")
        self.add_btn_two.clicked.connect(lambda: self.add_stat_wid(flag=Cfg.FILE_FOLDER))
        self.add_btn_two.setFixedWidth(150)
        btns_lay.addWidget(self.add_btn_two)
        
        self.add_btn_two = QPushButton("Остальное")
        self.add_btn_two.clicked.connect(lambda: self.add_stat_wid(flag=Cfg.MAIN_FOLDER))
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

        if flag == Cfg.NAMED_FOLDER:
            wid = StatWid(flag=Cfg.NAMED_FOLDER)

        elif flag == Cfg.FILE_FOLDER:

            if dest is None:
                dest = QFileDialog.getExistingDirectory(self)

            if dest:
                wid = StatWid(flag=Cfg.FILE_FOLDER, dest=dest)
            else:
                return
            
        elif flag == Cfg.MAIN_FOLDER:
            wid = StatWid(flag=Cfg.NAMED_FOLDER)

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

    def get_total_data(self) -> list[dict]:
        total_data = defaultdict(list)

        for wid in self.stat_wids:

            data = wid.get_data()

            if data is None:
                return None

            else:
                total_data[data.get(Cfg.FLAG)].append(
                    {
                        Cfg.SRC: data.get(Cfg.SRC),
                        Cfg.MAX_SIZE_KB: data.get(Cfg.MAX_SIZE_KB)
                    }
                )

        return total_data

    def start_btn_cmd(self):

        if not self.stat_wids:
            self.show_warning("Добавьте условия")
            return

        if not self.main_folder:
            self.show_warning("Укажите папку")
            return

        data = self.get_total_data()

        if not data:
            t = [
                    "Заполните все данные в условиях",
                    "Слева имя папки, справа целое число"
                ]
            self.show_warning("\n".join(t))

        self.task = StatementTask(
            main_folder = self.main_folder,
            data = data
        )
        # self.task.finished.connect(self.finished_task)
        self.task.start()

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
                    self.show_warning("Файл / папка должны быть в главной папке")

        super().dropEvent(a0)
