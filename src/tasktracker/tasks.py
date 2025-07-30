import json
import os
from datetime import datetime
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class Task:
    """A task with description, status, and timestamps.
    
    Attributes:
        description: The task description text.
        status: Current status of the task ('todo', 'in-progress', 'done').
        id: Unique identifier for the task.
        index: Sequential index number for the task.
        createdAt: Timestamp when the task was created.
        updatedAt: Timestamp when the task was last updated.
    """
    description: str
    status: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    index: int = field(init=False, default=0)
    createdAt: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updatedAt: str = field(init=False, default="")
    
    def __post_init__(self) -> None:
        """Initialize updatedAt with the creation timestamp."""
        self.updatedAt = self.createdAt
    
    def __str__(self) -> str:
        """Return a string representation of the task.
        
        Returns:
            A formatted string containing task index, description, status, and creation time.
        """
        return f'{self.index}- {self.description} (Status: {self.status}) [Created at: {self.createdAt}]'


class Manager:
    """Manages task operations including CRUD operations and persistence.
    
    This class handles loading, saving, and manipulating tasks stored in a JSON file.
    
    Attributes:
        json_file: Path to the JSON file for task storage.
        tasks: List of Task objects currently managed.
    """
    
    def __init__(self, json_file: str = 'data/task_data.json') -> None:
        """Initialize the Manager with a JSON file path.
        
        Args:
            json_file: Path to the JSON file for storing tasks. Defaults to 'data/task_data.json'.
        """
        self.json_file = json_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Load tasks from the JSON file.
        
        Creates the necessary directories and file if they don't exist.
        Handles JSON decode errors by resetting to an empty task list.
        
        Raises:
            OSError: If there are issues creating directories or files.
        """
        self.tasks = []

        # Extract directory from json_file path and create it if needed
        json_dir = os.path.dirname(self.json_file)
        if json_dir and not os.path.exists(json_dir):
            os.makedirs(json_dir)  # Create all necessary parent directories
        
        # Create the JSON file if it doesn't exist
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as file:
                json.dump([], file)
        
        # Load existing tasks
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
        """Save all tasks to the JSON file.
        
        Raises:
            RuntimeError: If there's an error during the save operation.
        """
        try:
            tasks_data = [asdict(task) for task in self.tasks]
            with open(self.json_file, 'w') as file:
                json.dump(tasks_data, file, indent=2)

        except Exception as e:
            raise RuntimeError(f'Error saving tasks: {e}') from e
    
    def add_task(self, description: str, status: str = 'todo') -> Task:
        """Add a new task with the given description and status.
        
        Args:
            description: The task description text.
            status: The initial status of the task. Defaults to 'todo'.
                   Must be one of: 'todo', 'in-progress', 'done'.
        
        Returns:
            The newly created Task object.
        
        Raises:
            ValueError: If description is empty or status is invalid.
            RuntimeError: If there's an error adding the task.
        """
        status = status.lower()
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
        """Delete a task by its index number.
        
        Args:
            task_index: The index number of the task to delete.
        
        Returns:
            The deleted Task object.
        
        Raises:
            ValueError: If no task is found with the given index.
        """
        for i, task in enumerate(self.tasks):
            if task.index == int(task_index):
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                return deleted_task
        raise ValueError(f"No task found with index {task_index}")

    def update_task(self, task_index: int, **kwargs: str) -> Task:
        """Update a task's properties by its index number.
        
        Args:
            task_index: The index number of the task to update.
            **kwargs: Keyword arguments for properties to update.
                     Supported keys: 'description', 'status'.
        
        Returns:
            The updated Task object.
        
        Raises:
            ValueError: If no task is found with the given index.
        """
        for task in self.tasks:
            if task.index == int(task_index):
                if 'description' in kwargs:
                    task.description = kwargs['description']
                if 'status' in kwargs:
                    task.status = kwargs['status'].lower()
                task.updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_tasks()
                return task
        print(f"No task found with index {task_index}")
        raise ValueError(f"No task found with index {task_index}")
    
    def status(self, task_index: int, status: str) -> Task:
        """Update a task's status using predefined status commands.
        
        Args:
            task_index: The index number of the task to update.
            status: The status command to apply. Valid commands:
                   'mark-done', 'mark-todo', 'mark-in-progress'.
        
        Returns:
            The updated Task object.
        
        Raises:
            ValueError: If the status command is invalid or task not found.
        """
        if status == 'mark-done':
            return self.update_task(task_index=task_index, status='done')
        elif status == 'mark-todo':
            return self.update_task(task_index=task_index, status='todo')
        elif status == 'mark-in-progress':
            return self.update_task(task_index=task_index, status='in-progress')
        else:
            raise ValueError(f"Invalid status command: {status}")

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the manager.
        
        Returns:
            A list of all Task objects.
        """
        return self.tasks
    
    def list_all_tasks(self) -> None:
        """Print all tasks to the console.
        
        Prints each task using its string representation.
        """
        for task in self.tasks:
            print(task)

    def list_by_arg(self, status_filter: str) -> List[Task]:
        """Get tasks filtered by status.
        
        Args:
            status_filter: The status to filter by ('todo', 'in-progress', 'done').
        
        Returns:
            A list of Task objects matching the status filter.
            Returns empty list if no tasks match.
        """
        founded_tasks = [task for task in self.tasks if task.status == status_filter]
        
        if not founded_tasks:
            print(f"No tasks found with status '{status_filter}'")
            return []
        
        return founded_tasks
    
    def __str__(self) -> str:
        """Return a string representation of the Manager.
        
        Returns:
            A string indicating the number of tasks managed.
        """
        return f'Manager with {len(self.tasks)} tasks'