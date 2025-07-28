import click
from rich.console import Console
from .tasks import Manager


console = Console()
manager = Manager()


@click.group()
def cli():
    """Task CLI group."""
    pass

@cli.command()
@click.argument('task')
def add(task):
    """Add a new task."""
    manager.add_task(description=task, status='in progress')
    # write_tasks(a_task)
    console.print(f"Added task: {task}", style='magenta')


@cli.command()
@click.argument('id')
@click.argument('task')
def update(id, task):
    """Update a task by ID."""
    click.echo(f"Updated task {id} to: {task}")

@cli.command()
@click.argument('task')
def delete(task):
    """Delete a task."""
    click.echo(f"Deleted task: {task}")

@cli.command()
@click.argument('task')
def mark_in_progress(task):
    """Mark a task as in progress."""
    click.echo(f"Task in progress: {task}")

@cli.command()
@click.argument('task')
def mark_done(task):
    """Mark a task as done."""
    click.echo(f"Task done: {task}")

@cli.command()
@click.argument('status', required=False, default='')
def list(status):
    """List tasks by status (done, todo, in progress or all)."""
    status_map = {
        '':      ('[cyan]Listing all tasks[/]', manager.list_all_tasks()),
        'done':  ('[green]Listing done tasks[/]',),
        'todo':  ('[yellow]Listing todo tasks[/]',),
        'in-progress': ('[blue]Listing in-progress tasks[/]',)
    }
    status = status_map.get(status)
    if status:
        console.print(status)
    else:
        console.print('[red]Unknown status[/]')