from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from core.user_manager import UserManager

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login or Register")
        self.user_manager = UserManager()
        self.init_ui()
        self.username = None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(32, 32, 32, 32)
        title = QLabel("<b>Task Scheduler Login</b>")
        title.setStyleSheet("font-size: 22px; margin-bottom: 16px; text-align: center;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(self.user_input)
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)
        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

    def login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text()
        ok, msg = self.user_manager.login(username, password)
        if ok:
            self.username = username
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", msg)

    def register(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text()
        ok, msg = self.user_manager.register(username, password)
        if ok:
            QMessageBox.information(self, "Registration", msg)
        else:
            QMessageBox.warning(self, "Registration Failed", msg) 