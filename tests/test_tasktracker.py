import unittest
import os
import json
import tempfile
import shutil
from tasktracker.tasks import Manager



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
    pass


class TestDeleteTask(BaseTestCase):
    pass


class TestUpdateTask(BaseTestCase):
    pass


class TestStatus(BaseTestCase):
    pass


class TestListing(BaseTestCase):
    pass



if __name__ == '__main__':
    unittest.main()