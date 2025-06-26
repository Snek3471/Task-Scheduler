from datetime import datetime
from plyer import notification

class ReminderManager:
    def __init__(self, username, task_manager):
        self.username = username
        self.task_manager = task_manager

    def check_due(self):
        now = datetime.now().isoformat()
        due_tasks = [t for t in self.task_manager.get_tasks() if not t['completed'] and t['due'] <= now]
        for t in due_tasks:
            self.notify(t['title'])
        return due_tasks

    def notify(self, task_title):
        notification.notify(
            title="Task Reminder",
            message=f"Task Due: {task_title}",
            timeout=5
        ) 