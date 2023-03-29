from django.test import TestCase
from backend.src.todo.todo_model import Todo

class TodoModel(TestCase):
    def setUp(self):
        Todo.objects.create(title="Test1 Unitest")
        Todo.objects.create(title="Test2 Unitest")
        Todo.objects.create(title="Test3 Unitest")
        
    def test_get_method_todos_len(self):
        current_todos = Todo.objects.all().values()
        self.assertEqual(len(current_todos), 3)
    
    def test_get_method_todos(self):
        mock_data = {
            "id": 4,
            "title": "Test 4 Unitest",
            "isComplete": False
        }
        
        Todo.objects.create(title=mock_data['title'])
        actual = list(Todo.objects.filter(title=mock_data['title']).values())[0]
        self.assertEqual(actual, mock_data)
    
    def test_update_method_todos(self):
        current_mock_data = {
            "id": 1,
            "title": "Test1 Unitest",
            "isComplete": False
        }
        
        mock_data = {
            "id": 1,
            "title": "Fixed Test 1 Unitest",
            "isComplete": True
        }

        actual_1 = list(Todo.objects.filter(id=current_mock_data['id']).values())[0]
        self.assertEqual(actual_1, current_mock_data)
        Todo.objects.filter(id=mock_data['id']).update(title=mock_data['title'], isComplete=mock_data['isComplete'])
        actual_2 = list(Todo.objects.filter(id=mock_data['id']).values())[0]
        self.assertEqual(actual_2, mock_data)
    
    def test_delete_method_todos(self):
        mock_id = 1
        Todo.objects.filter(id=mock_id).delete()
        actual = list(Todo.objects.all().values())
        self.assertEqual(len(actual), 2)
    
    def test_create_method_todos(self):
        mock_data = {
            "id": 4,
            "title": "Created Test 1 Unitest",
            "isComplete": False
        }
        Todo.objects.create(title=mock_data['title'])
        actuals = list(Todo.objects.all().values())
        actual = list(Todo.objects.filter(id=4).values())[0]
        self.assertEqual(len(actuals), 4)
        self.assertEqual(actual, mock_data)