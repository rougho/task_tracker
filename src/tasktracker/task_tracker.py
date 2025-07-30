"""Command-line interface for the task tracker application.

This module provides the main CLI interface for managing tasks through various commands
like add, update, delete, list, and status changes.
"""

from .tasks import Manager
import argparse
from . import pretty_print

manager = Manager()


def _confirm_delete(task) -> bool:
    """Ask user for confirmation before deleting a task.
    
    Args:
        task: The Task object to be deleted.
        
    Returns:
        True if user confirms deletion, False otherwise.
    """
    print("\n - You are about to delete the following task:")
    pretty_print.print_table([task], "Task to Delete")
    
    while True:
        confirmation = input("\n - Are you sure you want to delete this task? This action cannot be undone! (y/N): ").strip().lower()
        
        if confirmation in ['y', 'yes']:
            return True
        elif confirmation in ['n', 'no', '']:
            return False
        else:
            print(" - Please enter 'y' for yes or 'n' for no.")


def _handle_delete_command(args: argparse.Namespace) -> None:
    """Handle the 'delete' command with user confirmation.
    
    Args:
        args: Parsed command line arguments containing task_index to delete.
    """
    try:
        # First, find and display the task to be deleted
        task_to_delete = None
        for task in manager.get_all_tasks():
            if task.index == args.task_index:
                task_to_delete = task
                break
        
        if not task_to_delete:
            print(f"Error: No task found with ID {args.task_index}")
            return
        
        # Ask for confirmation
        if _confirm_delete(task_to_delete):
            deleted_task = manager.delete_task(args.task_index)
            pretty_print.print_by_tasks_command('delete', task=deleted_task)
        else:
            print(" - Delete operation cancelled.\n")
            
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main entry point for the task tracker CLI application.
    
    Sets up argument parsing, defines all available commands and their parameters,
    and dispatches to appropriate command handlers based on user input.
    
    Commands available:
        - add: Add a new task with optional status
        - update: Update an existing task's description and status
        - delete: Delete a task by its ID
        - list: List all tasks or filter by status
        - mark-done: Mark a task as completed
        - mark-in-progress: Mark a task as in progress
        - mark-todo: Mark a task as todo
        # Note: Searching tasks by status is part of the 'list' command
    
    The function uses argparse to handle command-line arguments and a dictionary
    of lambda functions to dispatch commands to their respective handlers.
    
    Raises:
        SystemExit: When invalid arguments are provided or required arguments are missing.
    """
    METAVAR = 'todo | in-progress | done'

    parser = argparse.ArgumentParser(
        prog='task-cli',
        description="""Task Tracker CLI - A simple and efficient command-line task management tool
        
        Manage your tasks with ease using intuitive commands. Track task status,
        organize your workflow, and boost productivity from your terminal.""",
        epilog='''EXAMPLES:
        
        Basic Operations:
        task-cli add "Buy groceries"                    # Add a new task
        task-cli add "Learn Python" -s in-progress     # Add task with status
        task-cli list                                   # Show all tasks
        task-cli list done                              # Show completed tasks
        task-cli list todo                              # Show pending tasks
        task-cli list in-progress                       # Show active tasks
        
        Task Management:
        task-cli update 1 "Buy organic groceries"      # Update task description
        task-cli update 1 "Study Python" -s done       # Update description and status
        task-cli delete 1                               # Remove a task
        
        Status Updates:
        task-cli mark-done 1                            # Mark task as completed
        task-cli mark-in-progress 2                     # Mark task as active
        task-cli mark-todo 3                            # Mark task as pending
        
        TIPS:
        • Task IDs are shown in the first column when listing tasks
        • Use quotes around task descriptions with spaces
        • Status options: todo, in-progress, done
        • Commands are case-sensitive
        
        For more help on specific commands, use:
        task-cli <command> --help
        
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    

    subparsers = parser.add_subparsers(
        dest='command', 
        required=True,
        title='Available Commands',
        description='Choose a command to manage your tasks',
        help='Use "task-cli <command> --help" for detailed help on each command'
    )

    # Add task command with enhanced help
    add_task = subparsers.add_parser(
        'add', 
        help='Add a new task to your list',
        description='''Add a new task to your task list with optional status.
        
        The task will be assigned a unique ID automatically for future reference.
        By default, new tasks are created with 'todo' status.''',
        epilog='''Examples:
        task-cli add "Complete project report"
        task-cli add "Review code changes" --status in-progress
        task-cli add "Deploy to production" -s done''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    add_task.add_argument('task', help='Description of the task you want to add')
    add_task.add_argument(
        '-s', '--status', 
        help='Initial status of the task (default: %(default)s)', 
        choices=['todo', 'in-progress', 'done'], 
        default='todo', 
        metavar=METAVAR
    )

    # Update task command with enhanced help
    update_task = subparsers.add_parser(
        'update', 
        help='Update an existing task',
        description='''Update both the description and status of an existing task.
        
        Use the task ID (shown in list command) to specify which task to update.
        Both description and status can be modified in a single command.''',
        epilog='''Examples:
        task-cli update 1 "Updated task description"
        task-cli update 2 "Review and test code" --status in-progress
        task-cli update 3 "Completed deployment" -s done''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    update_task.add_argument('task_index', type=int, help='ID number of the task to update')
    update_task.add_argument('task', help='New description for the task')
    update_task.add_argument(
        '-s', '--status', 
        help='New status for the task (default: %(default)s)', 
        choices=['todo', 'in-progress', 'done'], 
        default='todo', 
        metavar=METAVAR
    )

    # Delete task command with enhanced help
    delete_task = subparsers.add_parser(
        'delete', 
        help='Delete a task permanently',
        description='''Permanently remove a task from your list.
        
        WARNING: This action cannot be undone! The system will show you the task
        details and ask for confirmation before proceeding with deletion.''',
        epilog='''Examples:
        task-cli delete 1    # Delete task with ID 1 (will ask for confirmation)
        task-cli delete 5    # Delete task with ID 5 (will ask for confirmation)
        
        Note: You will see the task details and be prompted to confirm deletion.''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    delete_task.add_argument('task_index', type=int, help='ID of the task to delete')

    # List tasks command with enhanced help
    list_tasks = subparsers.add_parser(
        'list', 
        help='Display your tasks',
        description='''Display all tasks or filter by status.
        
        Without any arguments, shows all tasks in a formatted table.
        Use status filters to see specific categories of tasks.''',
        epilog='''Examples:
        task-cli list                # Show all tasks
        task-cli list todo           # Show only pending tasks
        task-cli list in-progress    # Show only active tasks
        task-cli list done           # Show only completed tasks''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    list_tasks.add_argument(
        'search', 
        nargs='?',
        help='Filter tasks by status (optional)', 
        choices=['done', 'todo', 'in-progress'], 
        metavar=METAVAR
    )

    # Status change commands with enhanced help
    status_progress = subparsers.add_parser(
        'mark-in-progress', 
        help='Mark a task as in-progress',
        description='''Change a task status to 'in-progress'.
        
        Use this when you start working on a task. The task will be marked
        as actively being worked on and the updated timestamp will be set.''',
        epilog='''Examples:
        task-cli mark-in-progress 1    # Start working on task 1
        task-cli mark-in-progress 3    # Resume work on task 3''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    status_progress.add_argument('task_index', type=int, help='ID of the task to mark as in-progress')

    status_done = subparsers.add_parser(
        'mark-done', 
        help='Mark a task as completed',
        description='''Change a task status to 'done'.
        
        Use this when you finish a task. The task will be marked as completed
        and the updated timestamp will be set to track when it was finished.''',
        epilog='''Examples:
        task-cli mark-done 1    # Complete task 1
        task-cli mark-done 2    # Mark task 2 as finished''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    status_done.add_argument('task_index', type=int, help='ID of the task to mark as done')

    status_todo = subparsers.add_parser(
        'mark-todo', 
        help='Mark a task as todo',
        description='''Change a task status back to 'todo'.
        
        Use this to reset a task to pending status. Useful when you need to
        restart a task or move it back to the backlog.''',
        epilog='''Examples:
        task-cli mark-todo 1    # Reset task 1 to todo
        task-cli mark-todo 4    # Move task 4 back to pending''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    status_todo.add_argument('task_index', type=int, help='ID of the task to mark as todo')

    args = parser.parse_args()

    command_handlers = {
        'add': lambda: pretty_print.print_by_tasks_command('add', task=manager.add_task(args.task, status=args.status)),
        'update': lambda: pretty_print.print_by_tasks_command('update', task=manager.update_task(args.task_index, description=args.task, status=args.status)),
        'delete': lambda: _handle_delete_command(args),
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