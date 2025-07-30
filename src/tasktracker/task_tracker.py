# from rich.console import Console
from .tasks import Manager
import argparse
from . import pretty_print

# console = Console()
manager = Manager()


def main():
    METAVAR = 'todo | in-progress | done'

    parser = argparse.ArgumentParser(
        prog='task-cli',
        description="A simple command-line task tracker",
        epilog='''Examples:
        task-cli add "Buy groceries"
        task-cli list
        task-cli list done
        task-cli list in-progress
        task-cli list todo
        task-cli update 1 "Buy organic groceries" -s done
        task-cli delete 1
        task-cli mark-done 1
        
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    

    subparsers = parser.add_subparsers(dest='command', required=True)

    add_task = subparsers.add_parser('add', help='add a new task')
    add_task.add_argument('task', help='the task you want to add')
    add_task.add_argument('-s', '--status', help='status of your task (todo, in-progress, done) (default: %(default)s)', choices=['todo', 'in-progress', 'done'], default='todo', metavar=METAVAR)


    update_task = subparsers.add_parser('update', help='update an existing task', )
    update_task.add_argument('task_index', type = int,  help='The ID Number of the task you want to update')
    update_task.add_argument('-s', '--status', help='status of your task (todo, in-progress, done) (default: %(default)s)', choices=['todo', 'in-progress', 'done'], default='todo', metavar=METAVAR)
    update_task.add_argument('task', help='The new task')

    delete_task = subparsers.add_parser('delete', help='to delete a task using ID')
    delete_task.add_argument('task_index', type = int,  help='the task ID you want to delte')

    list_tasks = subparsers.add_parser('list', help='List all your tasks')
    list_tasks.add_argument('search', nargs='?',help='search tasks by its status', choices=['done', 'todo', 'in-progress'], metavar=METAVAR)



    status_progress = subparsers.add_parser('mark-in-progress', help='Mark a task as its in the process using its ID')
    status_progress.add_argument('task_index', type = int,  help='The ID of the task!')

    status_done = subparsers.add_parser('mark-done', help='Mark a Task as its done using its ID')
    status_done.add_argument('task_index', type = int,  help='The ID of the task!')

    status_todo = subparsers.add_parser('mark-todo', help='Mark a Task as todo using its ID')
    status_todo.add_argument('task_index', type = int,  help='The ID of the task!')
  

    args = parser.parse_args()

    command_handlers = {
        'add': lambda: pretty_print.print_by_tasks_command('add', task=manager.add_task(args.task, status=args.status)),
        'update': lambda: pretty_print.print_by_tasks_command('update', task=manager.update_task(args.task_index, description=args.task, status=args.status)),
        'delete': lambda: pretty_print.print_by_tasks_command('delete', task=manager.delete_task(args.task_index)),
        'list': lambda: pretty_print.print_table(manager.list_by_arg(args.search), 'Search Results') if args.search else pretty_print.print_table(manager.get_all_tasks(), 'All Tasks'),
        'mark-in-progress': lambda: pretty_print.print_by_tasks_command('status', task=manager.status(task_index=args.task_index, status=args.command)),
        'mark-done': lambda: pretty_print.print_by_tasks_command('status', task=manager.status(task_index=args.task_index, status=args.command)),
        'mark-todo': lambda: pretty_print.print_by_tasks_command('status', task=manager.status(task_index=args.task_index, status=args.command)),
        'search': lambda: pretty_print.print_table(manager.list_by_arg(args.search), 'Search Results'),
    }
    
    if args.command in command_handlers:
        command_handlers[args.command]()



if __name__ == "__main__":
    main()