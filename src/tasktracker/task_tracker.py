# from rich.console import Console
from .tasks import Manager
import argparse

# console = Console()
manager = Manager()


def main():
    parser = argparse.ArgumentParser(prog='task-cli',description="Adding Tasks to task-cli")
    subpursers = parser.add_subparsers(dest='command', required=True)

    add_task = subpursers.add_parser('add', help='add a new task')
    add_task.add_argument('task', help='the task you want to add')
    add_task.add_argument('-s', '--status', help='status of your task (todo, in-progress, done)', choices=['todo', 'in-progress', 'done'], default='todo')


    update_task = subpursers.add_parser('update', help='update an existing task')
    update_task.add_argument('task_index', type = int,  help='The ID Number of the task you want to update')
    update_task.add_argument('-s', '--status', help='status of your task (todo, in-progress, done)', choices=['todo', 'in-progress', 'done'], default='todo')
    update_task.add_argument('task', help='The new task')

    delete_task = subpursers.add_parser('delete', help='to delete a task using ID')
    delete_task.add_argument('task_index', type = int,  help='the task ID you want to delte')

    subpursers.add_parser('list', help='list your tasks')

    status_progress = subpursers.add_parser('mark-in-progress')
    status_progress.add_argument('task_index', type = int,  help='The ID of the task!')

    status_done = subpursers.add_parser('mark-done')
    status_done.add_argument('task_index', type = int,  help='The ID of the task!')

    status_todo = subpursers.add_parser('mark-todo')
    status_todo.add_argument('task_index', type = int,  help='The ID of the task!')
  

    args = parser.parse_args()

    command_handlers = {
        'add': lambda: manager.add_task(args.task, status=args.status),
        'update': lambda: manager.update_task(args.task_index, description=args.task, status=args.status),
        'delete': lambda: manager.delete_task(args.task_index),
        'list': lambda: manager.list_all_tasks(),
        'mark-in-progress': lambda: manager.status(task_index=args.task_index, status=args.command),
        'mark-done': lambda: manager.status(task_index=args.task_index, status=args.command),
        'mark-todo': lambda: manager.status(task_index=args.task_index, status=args.command)
    }
    
    if args.command in command_handlers:
        command_handlers[args.command]()



if __name__ == "__main__":
    main()