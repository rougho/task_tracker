import json
import os
from datetime import datetime
import uuid
from dataclasses import dataclass, field, asdict
from random import randint


@dataclass
class Task:
    description: str
    status: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    index: str = field(init=False, default="")
    createdAt: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updatedAt: str = field(init=False)
    
    def __post_init__(self):
        self.updatedAt = self.createdAt
    
    def __str__(self):
        return f'your task is {self.description} and created at {self.createdAt}'



class Manager:
    def __init__(self, json_file='data.json'):
        self.json_file = json_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(
                        description=task_data['description'],
                        status=task_data['status']
                    )
                    task.id = task_data.get('id', task.id)
                    task.index=task_data.get('index', task.index)
                    task.createdAt = task_data.get('createdAt', task.createdAt)
                    task.updatedAt = task_data.get('updatedAt', task.updatedAt)
                    self.tasks.append(task)

    
    def save_tasks(self):
        """Save tasks to JSON file"""
        tasks_data = [asdict(task) for task in self.tasks]
        with open(self.json_file, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        print(f"Saved {len(self.tasks)} tasks to {self.json_file}")
    
    def add_task(self, description, status='todo'):
        task = Task(description, status)
        max_index = 0
        for existing_task in self.tasks:
            try:
                current_index = int(existing_task.index)
                if current_index > max_index:
                    max_index = current_index
            except (ValueError, AttributeError):
                pass
        
        task.index = str(max_index + 1)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def delete_task(self, task_index):
        """Delete task by task index field"""
        try:
            for i, task in enumerate(self.tasks):
                if task.index == str(task_index):
                    deleted_task = self.tasks.pop(i)
                    self.save_tasks()
                    return deleted_task
        except:
            raise ValueError(f"No task found with index {task_index}")
    
    def update_task(self, task_index, **kwargs):
        for task in self.tasks:
            if task.index == str(task_index):
                if 'description' in kwargs:
                    task.description = kwargs['description']
                if 'status' in kwargs:
                    task.status = kwargs['status']
                task.updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_tasks()
                return task
        raise ValueError(f"No task found with index {task_index}")

    def get_all_tasks(self):
        return self.tasks
    
    def __str__(self):
        return f'TaskManager with {len(self.tasks)} tasks'