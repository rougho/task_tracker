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
    index: int = field(init=False, default=0)
    createdAt: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updatedAt: str = field(init=False, default="")
    
    def __post_init__(self):
        self.updatedAt = self.createdAt
    
    def __str__(self):
        return f'{self.index} - {self.description} (Status: {self.status}) [Created at: {self.createdAt}]'



class Manager:
    def __init__(self, json_file='data/task_data.json'):
        self.json_file = json_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as file:
                json.dump([], file)
        
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as file:
                    tasks_data = json.load(file)
                    if isinstance(tasks_data, dict) and not tasks_data:
                        tasks_data = []
                    
                    for task_data in tasks_data:
                        task = Task(
                            description=task_data['description'],
                            status=task_data['status']
                        )
                        task.id = task_data.get('id', task.id)
                        task.index = int(task_data.get('index', task.index))
                        task.createdAt = task_data.get('createdAt', task.createdAt)
                        task.updatedAt = task_data.get('updatedAt', task.updatedAt)
                        self.tasks.append(task)
            except json.JSONDecodeError:
                self.tasks = []
                with open(self.json_file, 'w') as file:
                    json.dump([], file)
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        tasks_data = [asdict(task) for task in self.tasks]
        with open(self.json_file, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        print(f"Saved {len(self.tasks)} tasks to {self.json_file}")
    
    def add_task(self, description, status='todo'):
        """ adding task, a description requred and staus is todo """
        task = Task(description, status)
        if self.tasks:
            max_index = self.tasks[-1].index
        else:
            max_index = 0
        
        task.index = max_index + 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def delete_task(self, task_index):
        """Delete task by task index field"""
        for i, task in enumerate(self.tasks):
            if task.index == int(task_index):
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                return deleted_task
        print(f"No task found with index {task_index}")
        return None

    def update_task(self, task_index, **kwargs):
        task_index=int(task_index)
        for task in self.tasks:
            if task.index == int(task_index):
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
    
    def list_all_tasks(self):
        for task in self.tasks:
            print(task)
    
    def __str__(self):
        return f'Manager with {len(self.tasks)} tasks'