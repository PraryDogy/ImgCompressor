import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit

class MyWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.layout = QHBoxLayout()
        self.label = QLabel("Label:")
        self.line_edit = QLineEdit(text)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.setLayout(self.layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Example")

        self.layout = QVBoxLayout()
        
        self.title_label = QLabel("Заголовок")
        self.layout.addWidget(self.title_label)
        
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)
        
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        self.setLayout(self.layout)
        
    def add_item(self):
        list_item = QListWidgetItem()
        custom_widget = MyWidget('text')
        list_item.setSizeHint(custom_widget.sizeHint())
        
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, custom_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
