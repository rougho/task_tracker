import unittest
import os
import json
import tempfile
import shutil
from tasktracker.tasks import Manager
import time



class BaseTestCase(unittest.TestCase):
    """Base test class with common setup and teardown."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_task_data.json')

    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

class TestLoadTasks(BaseTestCase):
    """Test cases for the load_tasks method."""

    def test_creates_data_directory_if_not_exists(self):
        """Test that load_tasks creates data directory if it doesn't exist."""
        data_dir = os.path.join(self.test_dir, 'data')
        json_file = os.path.join(data_dir, 'tasks.json')
        
        self.assertFalse(os.path.exists(data_dir))
        manager = Manager(json_file=json_file)
        
        self.assertTrue(os.path.exists(data_dir))
        self.assertTrue(os.path.exists(json_file))
        self.assertEqual(len(manager.tasks), 0)

    def test_creates_empty_json_file_if_not_exists(self):
        """Test that load_tasks creates empty JSON file if it doesn't exist."""
        manager = Manager(json_file=self.test_file)

        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, 'r') as file:
            data = json.load(file)
            self.assertEqual(data, [])
        
        self.assertEqual(len(manager.tasks), 0)

    def test_loads_valid_json_data(self):
        """Test that load_tasks correctly loads valid JSON data."""
        test_data = [
            {
                "description": "First test Task",
                "status": "todo",
                "id": "3bdc9d94-10ec-4674-9cb6-37dbcaa8e98b",
                "index": 1,
                "createdAt": "2025-07-29 09:28:12",
                "updatedAt": "2025-07-29 09:28:12"
            }
        ]
        
        with open(self.test_file, 'w') as file:
            json.dump(test_data, file)

        manager = Manager(json_file=self.test_file)
        
        self.assertEqual(len(manager.tasks), 1)
        task = manager.tasks[0]
        self.assertEqual(task.description, 'First test Task')
        self.assertEqual(task.id, '3bdc9d94-10ec-4674-9cb6-37dbcaa8e98b')

    def test_handles_corrupted_json(self):
        """Test that load_tasks handles corrupted JSON gracefully."""
        with open(self.test_file, 'w') as file:
            file.write('§$"!$Invalidjsonfile§$%{')

        manager = Manager(json_file=self.test_file)

        self.assertEqual(len(manager.tasks), 0)

        with open(self.test_file) as file:
            data = json.load(file)
            self.assertEqual(data, [])

    def test_handles_missing_optional_fields(self):
        """Test that load_tasks handles missing optional fields."""
        test_data = [{"description": "Test missing data", "status": "todo"}]

        with open(self.test_file, 'w') as file:
            json.dump(test_data, file)

        manager = Manager(json_file=self.test_file)

        self.assertEqual(len(manager.tasks), 1)
        task = manager.tasks[0]
        self.assertEqual(task.description, 'Test missing data')
        self.assertEqual(task.status, 'todo')
        self.assertIsNotNone(task.id)
        self.assertEqual(task.index, 0)

    def test_prevents_duplication_on_multiple_calls(self):
        """Test that calling load_tasks multiple times doesn't duplicate tasks."""
        test_data = [
            {
                "description": "First test Task",
                "status": "todo",
                "id": "3bdc9d94-10ec-4674-9cb6-37dbcaa8e98b",
                "index": 1,
                "createdAt": "2025-07-29 09:28:12",
                "updatedAt": "2025-07-29 09:28:12"
            }
        ]
        
        with open(self.test_file, 'w') as file:
            json.dump(test_data, file)
        
        manager = Manager(json_file=self.test_file)
        self.assertEqual(len(manager.tasks), 1)
        
        manager.load_tasks()
        self.assertEqual(len(manager.tasks), 1) 


class TestAddTask(BaseTestCase):
    
    def test_add_successfully_task(self):

        manager = Manager(self.test_file)

        a_task = manager.add_task('Test adding a task')

        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(a_task.description, 'Test adding a task')
        self.assertEqual(a_task.status, 'todo')
        self.assertEqual(a_task.index, 1)
        self.assertIsNotNone(a_task.id)

    def test_add_without_description(self):
        manager = Manager(self.test_file)

        with self.assertRaises(ValueError) as context:
            manager.add_task('')

        self.assertEqual(str(context.exception), 'Task description cannot be empty')
        self.assertEqual(len(manager.tasks), 0)

    def test_add_with_invalid_status(self):

        manager = Manager(self.test_file)

        with self.assertRaises(ValueError) as context:
            manager.add_task('Test invalid status task', 'InvalidStatus')

        self.assertEqual(str(context.exception), 'Invalid status: invalidstatus')
        self.assertEqual(len(manager.tasks), 0)

    def test_add_task_index_increamentation(self):

        manager = Manager(self.test_file)

        #Add Four different task
        task1= manager.add_task('First task')
        task2 = manager.add_task('Second task')
        task3=manager.add_task('Third task')
        task4=manager.add_task('Fourth task')

        #Check each task index number
        self.assertEqual(task1.index, 1)
        self.assertEqual(task2.index, 2)
        self.assertEqual(task3.index, 3)
        self.assertEqual(task4.index, 4)

        #Check the length of the task manager (Four task created so = 4)
        self.assertEqual(len(manager.tasks), 4)

    def test_task_persists(self):
        manager = Manager(self.test_file)

        manager.add_task('Test save tasks', 'in-progress')

        manager2 = Manager(self.test_file)

        self.assertEqual(manager2.tasks[0].description, 'Test save tasks')
        self.assertEqual(manager2.tasks[0].status, 'in-progress')
        self.assertEqual(len(manager.tasks), 1)





class TestDeleteTask(BaseTestCase):
    
    def test_delete_a_task(self):
    
        manager = Manager(self.test_file)

        manager.add_task('Test delete task')

        self.assertEqual(len(manager.tasks), 1)

        deleted_task = manager.delete_task(1)

        self.assertEqual(len(manager.tasks), 0)
        self.assertEqual(deleted_task.description, 'Test delete task')

    def test_delete_task_from_multiple(self):

        manager = Manager(self.test_file)

        manager.add_task('First delete index')
        manager.add_task('Second delete index')
        manager.add_task('Third delete index')

        deleted_task = manager.delete_task(1)

        self.assertEqual(len(manager.tasks), 2)
        self.assertEqual(deleted_task.description, 'First delete index')

        remaining = [task.description for task in manager.tasks]

        self.assertIn('Second delete index', remaining)
        self.assertIn('Third delete index', remaining)

        #Check that deleted task is not existing anymore
        self.assertNotIn('First delete index', remaining)

    def test_delete_not_found(self):

        manager = Manager(self.test_file)

        with self.assertRaises(ValueError) as context:
            manager.delete_task(1234)
        
        self.assertEqual(str(context.exception), "No task found with index 1234")



class TestUpdateTask(BaseTestCase):
    
    def test_update_description(self):
        manager = Manager(self.test_file)

        manager.add_task('First task to be updated') #task 1
        task2 = manager.add_task('Second task to be updated') #task 2
        manager.add_task('Third task to be updated')# task 3

        #Create a copy of the original created task for comparison after updating the original
        temp_task2 = task2
        
        #pause the process so that the timestamp
        #on the updated task be different then the original task
        time.sleep(2) 

        #Update the task with Index 2
        manager.update_task(2, description='Second task is updated!')

        self.assertEqual(task2.description, temp_task2.description)
        self.assertEqual(task2.status, temp_task2.status)
        self.assertEqual(task2.index, temp_task2.index)
        self.assertEqual(task2.createdAt, temp_task2.createdAt)
        self.assertNotEqual(task2.updatedAt, temp_task2.createdAt)

    def test_update_task_status(self):

        manager = Manager(self.test_file)

        manager.add_task('Testing status update', 'in-progress')

        manager.update_task(manager.tasks[0].index, status='done')

        self.assertEqual(manager.tasks[0].status, 'done')

    def test_update_task_not_found(self):

        manager = Manager(self.test_file)
        with self.assertRaises(ValueError) as context:
            manager.update_task(1234, description='Test update not found')
        self.assertEqual(str(context.exception), "No task found with index 1234")


class TestStatus(BaseTestCase):
    
    def test_marks(self):

        manager = Manager(self.test_file)
        manager.add_task('Test mark done')
        manager.status(1, 'mark-done')
        self.assertEqual(manager.tasks[0].status, 'done')

        manager.add_task('Test mark in-progress')
        manager.status(2, 'mark-in-progress')
        self.assertEqual(manager.tasks[1].status, 'in-progress')

        manager.add_task('Test mark todo')
        manager.status(3, 'mark-todo')
        self.assertEqual(manager.tasks[2].status, 'todo')    

    def test_status_invalid_command(self):

        manager = Manager(self.test_file)
        manager.add_task('Test invalid command')

        with self.assertRaises(ValueError) as context:
            manager.status(1, 'SomeInvalidStatus')

        self.assertEqual(str(context.exception), 'Invalid status command: SomeInvalidStatus')



class TestListing(BaseTestCase):
    
    def test_list_by_args(self):

        manager = Manager(self.test_file)

        manager.add_task("task1")
        manager.add_task("task2", "done")
        manager.add_task("task3")

        search = manager.list_by_arg('todo')
        
        self.assertIsNotNone(search)
        
        # print(f'my result: {search[0]} -- {search[1]}')
        
        self.assertEqual(len(search), 2)

        # Check first todo task
        self.assertEqual(search[0].description, 'task1')
        self.assertEqual(search[0].status, 'todo')

        # Check second todo task
        self.assertEqual(search[1].description, 'task3')
        self.assertEqual(search[1].status, 'todo')
            
    def test_empty_task_list(self):
        """Test listing when no tasks exist."""
        manager = Manager(self.test_file)

        # Test get_all_tasks with empty list
        all_tasks = manager.get_all_tasks()
        self.assertEqual(len(all_tasks), 0)
        self.assertIsInstance(all_tasks, list)

        # Test list_by_arg with empty list
        search = manager.list_by_arg('todo')

        if search is None:
            self.assertIsNone(search)
        else:
            self.assertEqual(len(search), 0)
            self.assertIsInstance(search, list)

        # Test list_all_tasks with empty list (should not crash)
        try:
            manager.list_all_tasks()
            # If we get here without exception, the test passes
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"list_all_tasks() with empty list raised an exception: {e}")

    def test_list_by_args_no_matches(self):
        """Test list_by_arg when tasks exist but none match the filter."""
        manager = Manager(self.test_file)
        
        # Add tasks with different statuses
        manager.add_task("task1", "done")
        manager.add_task("task2", "in-progress")
        
        # Search for status that doesn't exist
        search = manager.list_by_arg('todo')
        
        if search is None:
            self.assertIsNone(search)
        else:
            self.assertEqual(len(search), 0)
            self.assertIsInstance(search, list)

    def test_get_all_tasks_with_data(self):
        """Test get_all_tasks when tasks exist."""
        manager = Manager(self.test_file)
        
        manager.add_task("First task", "todo")
        manager.add_task("Second task", "done")
        manager.add_task("Third task", "in-progress")
        
        all_tasks = manager.get_all_tasks()
        
        self.assertEqual(len(all_tasks), 3)
        self.assertIsInstance(all_tasks, list)
        
        # Check that all tasks are present
        descriptions = [task.description for task in all_tasks]
        self.assertIn("First task", descriptions)
        self.assertIn("Second task", descriptions)
        self.assertIn("Third task", descriptions)
        

if __name__ == '__main__':
    unittest.main()