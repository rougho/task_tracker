import click

@click.group()
def cli():
    """Task CLI group."""
    pass

@cli.command()
@click.argument('task')
def add(task):
    """Add a new task."""
    click.echo(f"Added task: {task}")

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
    if status == '':
        click.echo('Listing all tasks')
    elif status == 'done':
        click.echo('Listing done tasks')
    elif status == 'todo':
        click.echo('Listing todo tasks')
    elif status == 'in-progress':
        click.echo('Listing todo tasks')
    else:
        click.echo('Unknown status')