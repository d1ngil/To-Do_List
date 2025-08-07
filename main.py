import json
import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

TODO_FILE="todo_data.json"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.listbox = QListView(self)
        self.textbox = QLineEdit(self)
        self.model = QStringListModel()
        self.add_button = QPushButton("Add", self)
        self.finish_button = QPushButton("Finish", self)
        self.delete_button = QPushButton("Delete", self)

        self.tasks = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("To-Do List App")
        self.setFixedSize(600, 400)
        self.textbox.setPlaceholderText("Washing Dishes etc.")
        self.listbox.setModel(self.model)

        hbox = QHBoxLayout()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.finish_button)
        hbox.addWidget(self.delete_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listbox)
        vbox.addWidget(self.textbox)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.add_button.clicked.connect(self.add_task)
        self.finish_button.clicked.connect(self.mark_done)
        self.delete_button.clicked.connect(self.delete_task)

        self.load_tasks()
        self.refresh_list()

    def load_tasks(self):
        if not os.path.exists(TODO_FILE):
            self.tasks = []
        with open(TODO_FILE, "r") as file:
            self.tasks = json.load(file)

    def save_tasks(self):
        with open(TODO_FILE, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def refresh_list(self):
        display_list = []
        for i, task in enumerate(self.tasks, start=1):
            status = "✅" if task["done"] else "❌"
            display_list.append(f"{i}. {task['title']} [{status}]")
        self.model.setStringList(display_list)

    def add_task(self):
        title = self.textbox.text().strip()
        if title:
            self.tasks.append({"title": title, "done": False})
            self.save_tasks()
            self.refresh_list()
            self.textbox.clear()
        else:
            QMessageBox.warning(self, "Error", "Invalid Task")

    def mark_done(self):
        index = self.listbox.currentIndex().row()
        if index >= 0 and index < len(self.tasks):
            self.tasks[index]["done"] = True
            self.save_tasks()
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Error", "You need to choose a task")


    def delete_task(self):
        index = self.listbox.currentIndex().row()
        if index >= 0 and index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Error", "Select a task to delete")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())