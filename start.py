import os
import subprocess
import sys
import traceback

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication


class System_:

    @classmethod
    def catch_error(cls, *args) -> None:

        STARS = "*" * 40
        ABOUT = "Отправьте это сообщение в telegram @evlosh или на почту loshkarev@miuz.ru"
        ERROR = traceback.format_exception(*args)

        SUMMARY_MSG = "\n".join([*ERROR, STARS, ABOUT])
        
        script = "applescripts/error_msg.scpt"
        subprocess.run(["osascript", script, SUMMARY_MSG])

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


from app_statement import AppStatement

app = QApplication(sys.argv)

if not os.path.exists("lib"):
    app.setWindowIcon(QIcon("icon.png"))

ex = AppStatement()
ex.show()
sys.exit(app.exec_())
