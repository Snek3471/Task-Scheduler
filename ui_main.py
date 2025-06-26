from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit,
    QLabel, QHBoxLayout, QDateTimeEdit, QMessageBox
)
from PyQt5.QtCore import QDateTime, QTimer
from task_manager import TaskManager
from reminder_manager import ReminderManager

class TaskSchedulerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Scheduler")
        self.setMinimumSize(450, 500)

        self.task_manager = TaskManager("data.json")
        self.reminder_manager = ReminderManager()

        self.init_ui()
        self.refresh_task_list()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task")
        layout.addWidget(self.task_input)

        self.reminder_input = QDateTimeEdit()
        self.reminder_input.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.reminder_input)

        add_button = QPushButton("Add Task with Reminder")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.edit_task)
        layout.addWidget(self.task_list)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(1000)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            remind_time = self.reminder_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            self.task_manager.add_task(task, remind_time)
            self.task_input.clear()
            self.refresh_task_list()
            self.status_label.setText(f"Added: '{task}'")

    def refresh_task_list(self):
        self.task_list.clear()
        for task, time in self.task_manager.get_tasks():
            self.task_list.addItem(f"{task} (⏰ {time})")

    def edit_task(self, item):
        original = item.text().split(" (⏰")[0]
        new_task, ok = QInputDialog.getText(self, "Edit Task", "Modify task:", text=original)
        if ok and new_task.strip():
            self.task_manager.update_task(original, new_task.strip())
            self.refresh_task_list()
            self.status_label.setText("Task updated.")

    def check_reminders(self):
        due = self.reminder_manager.check_due(self.task_manager.get_tasks())
        if due:
            QMessageBox.information(self, "Reminder", f"⏰ Task Due: {due}")