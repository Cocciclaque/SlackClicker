import json
import os

class SaveManager:
    def __init__(self, save_file):
        self.save_data = {}
        self.save_file = save_file
        self.load()

    def load(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                self.save_data = json.load(f)
        else:
            self.save_data = {}

    def save(self):
        with open(self.save_file, 'w') as f:
            json.dump(self.save_data, f, indent=4)

    def get(self, key, default=None):
        if self.has(key) == False:
            self.set(key, 0)
        return self.save_data.get(key, default)

    def set(self, key, value):
        self.save_data[key] = value
        self.save()  # You could remove this line if you prefer manual saving

    def increment(self, key, amount=1):
        self.save_data[key] = self.get(key, 0) + amount
        self.save()

    def has(self, key):
        return key in self.save_data

    def clear(self):
        self.save_data = {}
        self.save()
