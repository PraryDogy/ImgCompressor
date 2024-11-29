from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from wid_nostat import WidNoStat
from wid_stat import WidStat

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(560, 560)

        main_lay = QVBoxLayout()
        self.setLayout(main_lay)


        self.tab_bar = QTabWidget()
        main_lay.addWidget(self.tab_bar)

        app_simple = WidNoStat()
        app_stat = WidStat()

        self.tab_bar.addTab(app_simple, "Сжатие без условий")
        self.tab_bar.addTab(app_stat, "Сжатие по условиям")