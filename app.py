from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from app_simple import AppSimple
from app_statement import AppStatement

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(560, 400)

        main_lay = QVBoxLayout()
        self.setLayout(main_lay)


        self.tab_bar = QTabWidget()
        main_lay.addWidget(self.tab_bar)

        app_simple = AppSimple()
        app_stat = AppStatement()

        self.tab_bar.addTab(app_simple, "Сжатие без условий")
        self.tab_bar.addTab(app_stat, "Сжатие по условиям")