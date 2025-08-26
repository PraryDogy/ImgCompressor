from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QCheckBox
from wid_nostat import WidNoStat
from wid_stat import WidStat
from cfg import Cfg

class App(QWidget):
    def __init__(self):
        Cfg.init()

        super().__init__()
        self.setMinimumSize(560, 560)
        self.setWindowTitle(Cfg.app_name)

        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(5, 10, 5, 5)
        self.setLayout(main_lay)

        self.checkbox = QCheckBox(text="Игнорировать PNG")
        self.checkbox.clicked.connect(self.cmd)
        main_lay.addWidget(self.checkbox)

        if Cfg.ignore_png:
            self.checkbox.setChecked(True)

        self.tab_bar = QTabWidget()
        self.tab_bar.tabBarClicked.connect(self.setFocus)
        main_lay.addWidget(self.tab_bar)

        app_simple = WidNoStat()
        app_stat = WidStat()

        self.tab_bar.addTab(app_simple, "Сжатие без условий")
        self.tab_bar.addTab(app_stat, "Сжатие по условиям")

    def cmd(self):
        if Cfg.ignore_png:
            self.checkbox.setChecked(False)
            Cfg.ignore_png = False
        else:
            self.checkbox.setChecked(True)
            Cfg.ignore_png = True
        
        Cfg.write_json()