import json
import os
import hashlib

class UserManager:
    def __init__(self, user_file="data/users.json"):
        self.user_file = user_file
        os.makedirs(os.path.dirname(user_file), exist_ok=True)
        if not os.path.exists(user_file):
            with open(user_file, "w") as f:
                json.dump({}, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        users = self._load_users()
        if username in users:
            return False, "Username already exists."
        users[username] = self.hash_password(password)
        self._save_users(users)
        return True, "Registration successful."

    def login(self, username, password):
        users = self._load_users()
        if username not in users:
            return False, "User not found."
        if users[username] != self.hash_password(password):
            return False, "Incorrect password."
        return True, "Login successful."

    def _load_users(self):
        with open(self.user_file, "r") as f:
            return json.load(f)

    def _save_users(self, users):
        with open(self.user_file, "w") as f:
            json.dump(users, f, indent=2) 