import os
import sys
import traceback

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QTextEdit,
                             QVBoxLayout)


class System_:

    @classmethod
    def catch_error(cls, *args) -> None:

        STARS = "*" * 40
        ABOUT = "Отправьте это сообщение в telegram @evlosh или на почту loshkarev@miuz.ru"
        ERROR = traceback.format_exception(*args)

        SUMMARY_MSG = "\n".join([*ERROR, STARS, ABOUT])
        
        d = QDialog()
        d.setWindowTitle("Ошибка")
        l = QVBoxLayout(d)

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setPlainText(SUMMARY_MSG)
        l.addWidget(txt)

        l.addWidget(QPushButton("Закрыть", clicked=d.close))
        d.resize(500, 400)
        d.setFocus()
        d.exec_()

    @classmethod
    def set_plugin_path(cls) -> bool:
        #lib folder appears when we pack this project to .app with py2app
        if os.path.exists("lib"): 
            plugin_path = "lib/python3.11/PyQt5/Qt5/plugins"
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
            return True
        else:
            return False
        
    @classmethod
    def set_excepthook(cls) -> None:
        sys.excepthook = cls.catch_error


if System_.set_plugin_path():
    System_.set_excepthook()
System_.set_excepthook()

from app import App

app_ = QApplication(sys.argv)

if not os.path.exists("lib"):
    app_.setWindowIcon(QIcon("icon.png"))

ex = App()
ex.show()
sys.exit(app_.exec_())
