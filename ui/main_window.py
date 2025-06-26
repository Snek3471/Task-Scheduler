from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from ui.login import LoginDialog
from ui.task_view import TaskView
from ui.stats_view import StatsView
import sys

def launch_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    app.setStyleSheet("""
        QWidget {
            background-color: #23272e;
            color: #f8f8f2;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 15px;
        }
        QPushButton {
            background-color: #44475a;
            color: #f8f8f2;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #6272a4;
        }
        QLineEdit, QComboBox, QDateTimeEdit {
            background-color: #282a36;
            color: #f8f8f2;
            border: 1px solid #44475a;
            border-radius: 6px;
            padding: 6px;
        }
        QListWidget {
            background-color: #282a36;
            color: #f8f8f2;
            border-radius: 6px;
        }
        QLabel {
            color: #f8f8f2;
        }
        QDialog {
            background-color: #23272e;
        }
    """)
    login = LoginDialog()
    login.setWindowIcon(QIcon('icon.png'))
    if login.exec_() == LoginDialog.Accepted:
        main = MainWindow(login.username)
        main.show()
        sys.exit(app.exec_())

class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Task Scheduler - {username}")
        self.setMinimumSize(800, 700)
        self.username = username
        self.layout = QVBoxLayout(self)
        self.toggle_btn = QPushButton("Show Statistics")
        self.toggle_btn.clicked.connect(self.toggle_view)
        self.layout.addWidget(self.toggle_btn)
        self.task_view = TaskView(username)
        self.stats_view = StatsView(username)
        self.layout.addWidget(self.task_view)
        self.current_view = 'task'

    def toggle_view(self):
        if self.current_view == 'task':
            self.layout.removeWidget(self.task_view)
            self.task_view.hide()
            self.stats_view.refresh_stats()
            self.layout.addWidget(self.stats_view)
            self.stats_view.show()
            self.toggle_btn.setText("Show Tasks")
            self.current_view = 'stats'
        else:
            self.layout.removeWidget(self.stats_view)
            self.stats_view.hide()
            self.layout.addWidget(self.task_view)
            self.task_view.show()
            self.toggle_btn.setText("Show Statistics")
            self.current_view = 'task' 