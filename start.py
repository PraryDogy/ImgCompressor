import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from gui import MyApp

if __name__ == '__main__':

    if os.path.exists("lib"): 
        #lib folder appears when we pack this project to .app with py2app

        py_ver = sys.version_info
        py_ver = f"{py_ver.major}.{py_ver.minor}"

        plugin_path = os.path.join(
            "lib",
            f"python{py_ver}",
            "PyQt5",
            "Qt5",
            "plugins",
            )

        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

    app = QApplication(sys.argv)

    if not os.path.exists("lib"):
        app.setWindowIcon(QIcon("icon.png"))

    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
