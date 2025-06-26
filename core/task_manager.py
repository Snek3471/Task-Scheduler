import json
import os
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self, username):
        self.username = username
        self.file = f"data/tasks_{username}.json"
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def add_task(self, title, due, category=None, priority=None, recurrence=None, dependencies=None):
        tasks = self._load()
        task = {
            "title": title,
            "due": due,
            "category": category,
            "priority": priority,
            "recurrence": recurrence,  # e.g., 'daily', 'weekly', 'monthly', None
            "dependencies": dependencies or [],
            "completed": False,
            "created": datetime.now().isoformat()
        }
        tasks.append(task)
        self._save(tasks)

    def get_tasks(self, filter_by=None, search=None):
        tasks = self._load()
        if filter_by:
            for key, value in filter_by.items():
                tasks = [t for t in tasks if t.get(key) == value]
        if search:
            tasks = [t for t in tasks if search.lower() in t["title"].lower()]
        return tasks

    def update_task(self, idx, **kwargs):
        tasks = self._load()
        for key, value in kwargs.items():
            tasks[idx][key] = value
        self._save(tasks)

    def delete_task(self, idx):
        tasks = self._load()
        tasks.pop(idx)
        self._save(tasks)

    def complete_task(self, idx):
        self.update_task(idx, completed=True)

    def handle_recurrence(self):
        tasks = self._load()
        now = datetime.now()
        new_tasks = []
        for t in tasks:
            if t["recurrence"] and t["completed"]:
                due = datetime.fromisoformat(t["due"])
                if t["recurrence"] == "daily":
                    next_due = due + timedelta(days=1)
                elif t["recurrence"] == "weekly":
                    next_due = due + timedelta(weeks=1)
                elif t["recurrence"] == "monthly":
                    next_due = due + timedelta(days=30)
                else:
                    continue
                if now > next_due:
                    t["due"] = next_due.isoformat()
                    t["completed"] = False
                    new_tasks.append(t)
        if new_tasks:
            self._save(tasks + new_tasks)

    def _load(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def _save(self, tasks):
        with open(self.file, "w") as f:
            json.dump(tasks, f, indent=2) 