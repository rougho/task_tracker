"""Pretty printing utilities for the task tracker application.

This module provides formatted output functions for displaying tasks in tables
and showing user feedback messages for various task operations.
"""

from typing import List
from .colors import Color
from .tasks import Task


def print_table(tasks: List[Task], title: str = '') -> None:
    """Print tasks in a formatted table with optional title.
    
    Displays tasks in a well-formatted table with columns for ID, Task description,
    Status, Created At, and Updated At. Includes alternating row colors for better
    readability and handles empty task lists gracefully.
    
    Args:
        tasks: List of Task objects to display in the table.
        title: Optional title to display above the table. Defaults to empty string.
    
    Returns:
        None. Prints the formatted table directly to stdout.
    
    Example:
        >>> tasks = [task1, task2, task3]
        >>> print_table(tasks, "My Tasks")
        
        ================================
              My Tasks
        ================================
         ID | Task | Status | Created At | Updated At
        --------------------------------
         1  | Buy milk | todo | 2025-01-01 | 2025-01-01
         2  | Walk dog | done | 2025-01-01 | 2025-01-01
        ================================
    """
    if not tasks:
        print(f'{Color.RED} There is no task to display {Color.RESET}')
        return

    # Calculate column widths based on content
    index_width = max(len(str(task.index)) for task in tasks)
    task_width = max(len(task.description) for task in tasks)
    status_width = max(len(task.status) for task in tasks)
    createdAt_width = max(len(str(task.createdAt)) for task in tasks)
    updatedAt_width = max(len(str(task.updatedAt)) for task in tasks)

    # Ensure minimum widths for headers
    index_width = max(index_width, 3) 
    task_width = max(task_width, 4)
    status_width = max(status_width, 6)
    createdAt_width = max(createdAt_width, 10)
    updatedAt_width = max(updatedAt_width, 10)

    # Create table header
    header = (
        f" {'ID'.ljust(index_width)} | "
        f" {'Task'.ljust(task_width)} | "
        f" {'Status'.ljust(status_width)} | "
        f" {'Created At'.ljust(createdAt_width)} | "
        f" {'Updated At'.ljust(updatedAt_width)}"
    )

    # Calculate total header width for borders
    header_width = int(len(header)) 

    print('\n')
    if title:
        print(f"{'='*header_width}")
        print(f"{Color.BLUE}{title.center(header_width)}{Color.RESET}")
        print(f"{'='*header_width}")

    print(f"{Color.YELLOW}{header}{Color.RESET}")
    print('-' * header_width)

    # Print table rows with alternating colors
    for index, task in enumerate(tasks):
        if index % 2 == 0:
            # Even rows - normal formatting
            row = (
                f" {str(task.index).ljust(index_width)} | "
                f" {task.description.ljust(task_width)} | " 
                f" {task.status.ljust(status_width)} | "
                f" {str(task.createdAt).ljust(createdAt_width)} | "
                f" {str(task.updatedAt).ljust(updatedAt_width)}"
            )
        else:
            # Odd rows - highlighted background
            row = (
                f"{Color.BG_CYAN} {Color.BLACK}{str(task.index).ljust(index_width)} | "
                f"{Color.BG_CYAN} {Color.BLACK}{task.description.ljust(task_width)} | " 
                f"{Color.BG_CYAN} {Color.BLACK}{task.status.ljust(status_width)} | "
                f"{Color.BG_CYAN} {Color.BLACK}{str(task.createdAt).ljust(createdAt_width)} | "
                f"{Color.BG_CYAN} {Color.BLACK}{str(task.updatedAt).ljust(updatedAt_width)}{Color.RESET}"
            )

        print(row)
    print('=' * header_width)
    print('\n')


def print_by_tasks_command(command: str, **kwargs) -> None:
    """Print formatted success messages for task operations.
    
    Displays color-coded success messages for various task operations including
    add, delete, update, and status changes. Each message type has specific
    formatting and visual indicators.
    
    Args:
        command: The operation type. Valid values are 'add', 'delete', 'update', 'status'.
        **kwargs: Keyword arguments containing operation-specific data.
                 Expected to contain 'task' key with a Task object.
    
    Returns:
        None. Prints the formatted message directly to stdout.
    
    Raises:
        KeyError: If 'task' key is not found in kwargs.
        AttributeError: If the task object doesn't have required attributes.
    
    Example:
        >>> task = Task("Buy groceries", "todo")
        >>> print_by_tasks_command('add', task=task)
        
        ------------------------------
        ✓ - Your Task -> Buy groceries
          - with ID number -> 1
          - has been successfully added!
        ------------------------------
    """
    if 'task' in kwargs:
        task = kwargs['task']

        print('\n')
        # Create border based on task description length plus padding
        border_length = (len(kwargs['task'].description)) + 30
        print('-' * border_length)
        
        if command == 'add':
            print(f'{Color.GREEN} ✓{Color.RESET} - Your Task -> {Color.GREEN}{task.description}{Color.RESET} \n   - with ID number -> {Color.GREEN}{task.index}{Color.RESET} \n   - has been successfully added!')

        elif command == 'delete':
            print(f'{Color.RED} ✗{Color.RESET} - Your Task -> {Color.RED}{task.description}{Color.RESET} \n   - with ID number -> {Color.RED}{task.index}{Color.RESET} \n   - has been successfully Deleted!!')

        elif command == 'update':
            print(f'{Color.GREEN} ✓{Color.RESET} - The Task with the ID number -> {Color.BLUE}{task.index}{Color.RESET} \n   - has been {Color.GREEN}successfully{Color.RESET} Updated!!')

        elif command == 'status':
            print(f'{Color.GREEN} ✓{Color.RESET} - Your Task Status with ID {task.index} has been {Color.GREEN}successfully{Color.RESET} updated!!')
        
        print('-' * border_length)
        print('\n')

