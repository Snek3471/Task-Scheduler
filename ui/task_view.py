from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QComboBox, QDateTimeEdit, QMessageBox, QFileDialog, QFrame)
from PyQt5.QtCore import QDateTime, QTimer
from core.task_manager import TaskManager
from core.reminder_manager import ReminderManager
from datetime import datetime
import csv

class TaskView(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.task_manager = TaskManager(username)
        self.reminder_manager = ReminderManager(username, self.task_manager)
        self.init_ui()
        self.refresh_task_list()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(10000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        # Section: Add Task
        add_section = QVBoxLayout()
        add_label = QLabel("<b>Add New Task</b>")
        add_label.setStyleSheet("font-size: 17px; margin-bottom: 8px;")
        add_section.addWidget(add_label)
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Task title")
        add_section.addWidget(self.task_input)
        due_label = QLabel("Due Date & Time:")
        add_section.addWidget(due_label)
        self.due_input = QDateTimeEdit()
        self.due_input.setCalendarPopup(True)
        self.due_input.setDisplayFormat("dd MMM yyyy, hh:mm AP")
        now = QDateTime.currentDateTime()
        self.due_input.setDateTime(now)
        self.due_input.setMinimumDateTime(now)
        self.due_input.setToolTip("Pick the date and time when the task is due. Click the calendar icon to select a date.")
        add_section.addWidget(self.due_input)
        due_help = QLabel("<i>Click the calendar icon to pick a date. Use the time field to set the exact due time.</i>")
        due_help.setStyleSheet("font-size: 12px; color: #bbbbbb; margin-bottom: 4px;")
        add_section.addWidget(due_help)
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category (optional)")
        add_section.addWidget(self.category_input)
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        add_section.addWidget(self.priority_input)
        self.recur_input = QComboBox()
        self.recur_input.addItems(["None", "Daily", "Weekly", "Monthly"])
        add_section.addWidget(self.recur_input)
        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_task)
        add_section.addWidget(add_btn)
        add_frame = QFrame()
        add_frame.setLayout(add_section)
        add_frame.setFrameShape(QFrame.StyledPanel)
        add_frame.setStyleSheet("QFrame { border: 1px solid #44475a; border-radius: 8px; padding: 12px; }")
        layout.addWidget(add_frame)
        # Section: Search/Filter
        search_label = QLabel("<b>Search & Filter</b>")
        search_label.setStyleSheet("font-size: 16px; margin-top: 8px;")
        layout.addWidget(search_label)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks")
        search_layout.addWidget(self.search_input)
        filter_btn = QPushButton("Search/Filter")
        filter_btn.clicked.connect(self.refresh_task_list)
        search_layout.addWidget(filter_btn)
        layout.addLayout(search_layout)
        # Section: Export/Import
        expimp_layout = QHBoxLayout()
        export_btn = QPushButton("Export Tasks (CSV)")
        export_btn.clicked.connect(self.export_tasks)
        expimp_layout.addWidget(export_btn)
        import_btn = QPushButton("Import Tasks (CSV)")
        import_btn.clicked.connect(self.import_tasks)
        expimp_layout.addWidget(import_btn)
        layout.addLayout(expimp_layout)
        # Section: Task List
        list_label = QLabel("<b>Task List</b>")
        list_label.setStyleSheet("font-size: 16px; margin-top: 8px;")
        layout.addWidget(list_label)
        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.edit_task)
        layout.addWidget(self.task_list)
        # Complete/delete buttons
        btn_layout = QHBoxLayout()
        complete_btn = QPushButton("Complete Task")
        complete_btn.clicked.connect(self.complete_task)
        btn_layout.addWidget(complete_btn)
        delete_btn = QPushButton("Delete Task")
        delete_btn.clicked.connect(self.delete_task)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)
        # Status
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

    def add_task(self):
        title = self.task_input.text().strip()
        due_qt = self.due_input.dateTime()
        now = QDateTime.currentDateTime()
        if due_qt < now:
            self.status_label.setText("Due date/time cannot be in the past.")
            return
        due = due_qt.toString("yyyy-MM-ddTHH:mm:ss")
        category = self.category_input.text().strip() or None
        priority = self.priority_input.currentText()
        recur = self.recur_input.currentText().lower()
        if recur == "none":
            recur = None
        if not title:
            self.status_label.setText("Task title required.")
            return
        self.task_manager.add_task(title, due, category, priority, recur)
        self.task_input.clear()
        self.refresh_task_list()
        self.status_label.setText(f"Added: {title}")

    def refresh_task_list(self):
        search = self.search_input.text().strip()
        tasks = self.task_manager.get_tasks(search=search if search else None)
        self.task_list.clear()
        for i, t in enumerate(tasks):
            status = "✔" if t["completed"] else "✗"
            self.task_list.addItem(f"{i+1}. {t['title']} [{t.get('category','')}] ({t.get('priority','')}) {status} (Due: {t['due']})")

    def edit_task(self, item):
        idx = self.task_list.currentRow()
        tasks = self.task_manager.get_tasks()
        t = tasks[idx]
        new_title, ok = QInputDialog.getText(self, "Edit Task", "Modify task:", text=t["title"])
        if ok and new_title.strip():
            self.task_manager.update_task(idx, title=new_title.strip())
            self.refresh_task_list()
            self.status_label.setText("Task updated.")

    def complete_task(self):
        idx = self.task_list.currentRow()
        if idx < 0:
            return
        self.task_manager.complete_task(idx)
        self.refresh_task_list()
        self.status_label.setText("Task completed.")

    def delete_task(self):
        idx = self.task_list.currentRow()
        if idx < 0:
            return
        self.task_manager.delete_task(idx)
        self.refresh_task_list()
        self.status_label.setText("Task deleted.")

    def check_reminders(self):
        due = self.reminder_manager.check_due()
        if due:
            QMessageBox.information(self, "Reminder", f"⏰ Task Due: {due[0]['title']}")

    def export_tasks(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Tasks", "", "CSV Files (*.csv)")
        if not path:
            return
        tasks = self.task_manager.get_tasks()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
            writer.writeheader()
            writer.writerows(tasks)
        self.status_label.setText(f"Exported to {path}")

    def import_tasks(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Tasks", "", "CSV Files (*.csv)")
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.task_manager.add_task(
                    row['title'], row['due'], row.get('category'), row.get('priority'), row.get('recurrence'), row.get('dependencies')
                )
        self.refresh_task_list()
        self.status_label.setText(f"Imported from {path}") 