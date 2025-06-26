from PyQt5.QtCore import QDateTime

class ReminderManager:
    def check_due(self, tasks):
        current = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        for task, time in tasks:
            if time == current:
                return task
        return None