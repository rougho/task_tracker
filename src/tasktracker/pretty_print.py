from typing import List
from .colors import Color
from .tasks import Task



def print_table(tasks: List[Task], title: str = '') -> None:
    if not tasks:
        print(f'{Color.RED} There is no task to display {Color.RESET}')
        return

    # Calculate column widths
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

    header = (
        f" {'ID'.ljust(index_width)} | "
        f" {'Task'.ljust(task_width)} | "
        f" {'Status'.ljust(status_width)} | "
        f" {'Created At'.ljust(createdAt_width)} | "
        f" {'Updated At'.ljust(updatedAt_width)}"
    )

    # Header
    header_width = int(len(header)) 

    print('\n')
    if title:
        print(f"{'='*header_width}")
        print(f"{Color.BLUE}{title.center(header_width)}{Color.RESET}")
        print(f"{'='*header_width}")

    print(f"{Color.YELLOW}{header}{Color.RESET}")
    print('-' * header_width)

    # Rows
    for index, task in enumerate(tasks):
        if index % 2 == 0:
            row = (
                f" {str(task.index).ljust(index_width)} | "
                f" {task.description.ljust(task_width)} | " 
                f" {task.status.ljust(status_width)} | "
                f" {str(task.createdAt).ljust(createdAt_width)} | "
                f" {str(task.updatedAt).ljust(updatedAt_width)}"
            )
        else:
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

    if 'task' in kwargs:

        task = kwargs['task']

        print('\n')
        print('-' * ((len(kwargs['task'].description))+ 30))
        if command == 'add':
            print(f'{Color.GREEN} ✓{Color.RESET} - Your Task -> {Color.GREEN}{task.description}{Color.RESET} \n   - with ID number -> {Color.GREEN}{task.index}{Color.RESET} \n   - has been successfully added!')

        if command == 'delete':
            print(f' {Color.RED}✗ {Color.RESET} - Your Task -> {Color.RED}{task.description}{Color.RESET} \n   - with ID number -> {Color.RED}{task.index}{Color.RESET} \n   - has been successfully Deleted!!')

        if command == 'update':
            print(f'{Color.GREEN} ✓{Color.RESET} - The Task with the ID number -> {Color.BLUE}{task.index}{Color.RESET} \n   - has been {Color.GREEN}successfully{Color.RESET} Updated!!')

        if command == 'status':
            print(f'{Color.GREEN} ✓{Color.RESET} - Your Task Status with ID {task.index} has been {Color.GREEN}successfully{Color.RESET} updated!!')
        

        print('-' * ((len(kwargs['task'].description))+ 30))
        print('\n')

