from django.test import TestCase
from django.http import JsonResponse
from backend.src.todo.todo_controller import todo_controller
from backend.src.todo.todo_model import Todo
import json

class MockWSGI:
    
    def __init__(self, method, body, headers):
        self.method = method
        self.body = body
        self.headers = headers
    

class TodoModel(TestCase):
    def setUp(self):
        Todo.objects.create(title="Test1 Unitest")
        Todo.objects.create(title="Test2 Unitest")
        Todo.objects.create(title="Test3 Unitest")
        self.mock_data = [
            {
                "id": 1,
                "title": "Test1 Unitest",
                "isComplete": False
            },
            {
                "id": 2,
                "title": "Test2 Unitest",
                "isComplete": False
            },
            {
                "id": 3,
                "title": "Test3 Unitest",
                "isComplete": False
            },
        ]
        
    def test_get_request(self):
        request = MockWSGI(method="GET", body=b"", headers={})
        actual_response = todo_controller(request)
        actual_response = json.loads(actual_response.content)
        self.assertEqual(actual_response, self.mock_data)
    
    def test_post_request(self):
        mock_post_data = b'{"id": 4,"title": "Create Test 4 Unitest","isComplete": false}'
        request = MockWSGI(method="POST", body=mock_post_data, headers={})
        mock_response = todo_controller(request)
        request = MockWSGI(method="GET", body=b"", headers={})
        actual_response = todo_controller(request)
        actual_response = json.loads(actual_response.content)
        self.mock_data.append(json.loads(mock_post_data))
        self.assertEqual(actual_response, self.mock_data)