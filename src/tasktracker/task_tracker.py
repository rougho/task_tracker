# import click
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

    update_task = subpursers.add_parser('update', help='update an existing task')
    update_task.add_argument('task_id', help='The ID Number of the task you want to update')
    update_task.add_argument('-s', '--status', help='status of your task')
    update_task.add_argument('task', help='The new task')

    args = parser.parse_args()

    if args.command == 'add':
        manager.add_task(args.task)
    if args.command == 'update':
        manager.update_task(args.task_id, description=args.task, status=args.status)


if __name__ == "__main__":
    main()

# @click.group()
# def cli():
#     """Task CLI group."""
#     pass

# @cli.command()
# @click.argument('task')
# def add(task):
#     """Add a new task."""
#     manager.add_task(description=task, status='in progress')
#     # write_tasks(a_task)
#     console.print(f"Added task: {task}", style='magenta')


# @cli.command()
# @click.argument('id')
# @click.argument('task')
# @click.option('--status', '-s', help='update tasks status')
# def update(id, task, status):
#     """Update a task by ID."""
#     manager.update_task(int(id), description=task, status=status)
#     click.echo(f"Updated task {id} to: {task} with status: {status}")


# @cli.command()
# @click.argument('task')
# def delete(task):
#     """Delete a task."""
#     manager.delete_task(task)
#     click.echo(f"Deleted task: {task}")

# @cli.command()
# @click.argument('task')
# def mark_in_progress(task):
#     """Mark a task as in progress."""
#     click.echo(f"Task in progress: {task}")

# @cli.command()
# @click.argument('task')
# def mark_done(task):
#     """Mark a task as done."""
#     click.echo(f"Task done: {task}")

# @cli.command()
# @click.argument('status', required=False, default='')
# def list(status):
#     """List tasks by status (done, todo, in progress or all)."""
#     status_map = {
#         '':      ('[cyan]Listing all tasks[/]', manager.list_all_tasks()),
#         'done':  ('[green]Listing done tasks[/]',),
#         'todo':  ('[yellow]Listing todo tasks[/]',),
#         'in-progress': ('[blue]Listing in-progress tasks[/]',)
#     }
#     status = status_map.get(status)
#     if status:
#         console.print(status)
#     else:
#         console.print('[red]Unknown status[/]')