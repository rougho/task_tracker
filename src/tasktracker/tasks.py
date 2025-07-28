import json
import os
from datetime import datetime
import uuid
from dataclasses import dataclass, field, asdict
from typing import List
from .colors import Color

@dataclass
class Task:
    description: str
    status: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    index: int = field(init=False, default=0)
    createdAt: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updatedAt: str = field(init=False, default="")
    
    def __post_init__(self) -> None:
        self.updatedAt = self.createdAt
    
    def __str__(self) -> str:
        return f'{Color.GREEN}{self.index}{Color.RESET} - {self.description} (Status: {self.status}) [Created at: {self.createdAt}]'



class Manager:
    def __init__(self, json_file='data/task_data.json'):
        self.json_file = json_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Load tasks from JSON file"""
        if not os.path.isdir('data'):
            os.mkdir('data')
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
    
    def save_tasks(self) -> None:
        """Save tasks to JSON file"""
        try:
            tasks_data = [asdict(task) for task in self.tasks]
            with open(self.json_file, 'w') as file:
                json.dump(tasks_data, file, indent=2)
        except Exception as e:
            raise RuntimeError(f'Error saving tasks: {e}') from e
    
    def add_task(self, description: str, status: str = 'todo') -> Task:
        """Add a task with description and status"""
        if not description.strip():
            raise ValueError("Task description cannot be empty")
        
        if status not in ['todo', 'in-progress', 'done']:
            raise ValueError(f"Invalid status: {status}")
        
        try:
            task = Task(description, status)
            if self.tasks:
                max_index = self.tasks[-1].index
            else:
                max_index = 0
            
            task.index = max_index + 1
            self.tasks.append(task)
            self.save_tasks()
            return task
        
        except Exception as e:
            raise RuntimeError(f"Failed to add task: {e}") from e
    
    def delete_task(self, task_index: int) -> Task:
        """Delete task by task index field"""
        for i, task in enumerate(self.tasks):
            if task.index == int(task_index):
                self.tasks.pop(i)
                self.save_tasks()
                print(f'The task with the ID number {i} were deleted')
        raise ValueError(f"No task found with index {task_index}")

    def update_task(self, task_index: int, **kwargs: str) -> object:
        for task in self.tasks:
            if task.index == int(task_index):
                if 'description' in kwargs:
                    task.description = kwargs['description']
                if 'status' in kwargs:
                    task.status = kwargs['status']
                task.updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_tasks()
                return task
        print(f"No task found with index {task_index}")
    
    def status(self, task_index: int, status: str) -> None:
        if status == 'mark-done':
            self.update_task(task_index=task_index, status='done')
        elif status == 'mark-todo':
            self.update_task(task_index=task_index, status='todo')
        elif status == 'mark-in-progress':
            self.update_task(task_index=task_index, status='in-progress')
        else:
            raise ValueError(f"Invalid status command: {status}")


    def get_all_tasks(self) -> List[Task]:
        return self.tasks
    
    def list_all_tasks(self) -> None:
        for task in self.tasks:
            print(task)

    def list_by_arg(self, status_filter: str) -> None:
        """List tasks filtered by status"""
        founded_tasks = [task for task in self.tasks if task.status == status_filter]
        
        if not founded_tasks:
            print(f"No tasks found with status '{status_filter}'")
            return
        
        for task in founded_tasks:
            print(task)
    
    def __str__(self) -> str:
        return f'Manager with {len(self.tasks)} tasks'