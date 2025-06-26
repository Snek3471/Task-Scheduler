import json
import os

class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.tasks = json.load(file)
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, task, reminder_time):
        self.tasks.append([task, reminder_time])
        self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def update_task(self, old_task, new_task):
        for i, (t, time) in enumerate(self.tasks):
            if t == old_task:
                self.tasks[i][0] = new_task
                break
        self.save_tasks()