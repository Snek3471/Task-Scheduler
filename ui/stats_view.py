from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from datetime import datetime
from core.task_manager import TaskManager

class StatsView(QWidget):
    def __init__(self, username):
        super().__init__()
        self.task_manager = TaskManager(username)
        self.init_ui()
        self.refresh_stats()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.total_label = QLabel()
        self.completed_label = QLabel()
        self.overdue_label = QLabel()
        self.by_category_label = QLabel()
        self.by_priority_label = QLabel()
        layout.addWidget(self.total_label)
        layout.addWidget(self.completed_label)
        layout.addWidget(self.overdue_label)
        layout.addWidget(self.by_category_label)
        layout.addWidget(self.by_priority_label)

    def refresh_stats(self):
        tasks = self.task_manager.get_tasks()
        total = len(tasks)
        completed = sum(1 for t in tasks if t['completed'])
        now = datetime.now().isoformat()
        overdue = sum(1 for t in tasks if not t['completed'] and t['due'] < now)
        by_category = {}
        by_priority = {}
        for t in tasks:
            cat = t.get('category') or 'Uncategorized'
            by_category[cat] = by_category.get(cat, 0) + 1
            prio = t.get('priority') or 'None'
            by_priority[prio] = by_priority.get(prio, 0) + 1
        self.total_label.setText(f"Total tasks: {total}")
        self.completed_label.setText(f"Completed: {completed}")
        self.overdue_label.setText(f"Overdue: {overdue}")
        self.by_category_label.setText(f"By category: {by_category}")
        self.by_priority_label.setText(f"By priority: {by_priority}") 