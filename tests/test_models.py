import pytest
from datetime import datetime, timedelta
from models.task import Task
from models.project import Project
from models.user import User

class TestTask:
    def test_create_task(self):
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Test Task", "Description", 1, due_date, 1, 1)
        assert task.title == "Test Task"
        assert task.priority == 1
        assert task.status == "pending"
    
    def test_update_status(self):
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Test", "Desc", 2, due_date, 1, 1)
        assert task.update_status("in_progress") == True
        assert task.status == "in_progress"
        assert task.update_status("invalid") == False
    
    def test_is_overdue(self):
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)
        task1 = Task("Overdue", "Desc", 1, past_date, 1, 1)
        task2 = Task("Not Overdue", "Desc", 1, future_date, 1, 1)
        assert task1.is_overdue() == True
        assert task2.is_overdue() == False
    
    def test_to_dict(self):
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Test", "Desc", 3, due_date, 2, 3)
        task.id = 42
        d = task.to_dict()
        assert d['id'] == 42
        assert d['title'] == "Test"
        assert d['priority'] == 3

class TestProject:
    def test_create_project(self):
        start = datetime.now()
        end = datetime.now() + timedelta(days=30)
        project = Project("Project A", "Description", start, end)
        assert project.name == "Project A"
        assert project.status == "active"
    
    def test_update_status(self):
        start = datetime.now()
        end = datetime.now() + timedelta(days=30)
        project = Project("P", "D", start, end)
        assert project.update_status("completed") == True
        assert project.status == "completed"
    
    def test_to_dict(self):
        start = datetime.now()
        end = datetime.now() + timedelta(days=30)
        project = Project("P", "D", start, end)
        project.id = 5
        d = project.to_dict()
        assert d['id'] == 5
        assert d['name'] == "P"

class TestUser:
    def test_create_user(self):
        user = User("john", "john@mail.com", "developer")
        assert user.username == "john"
        assert user.role == "developer"
    
    def test_update_info(self):
        user = User("john", "john@mail.com", "developer")
        user.update_info(username="john_updated", email="new@mail.com")
        assert user.username == "john_updated"
        assert user.email == "new@mail.com"
    
    def test_to_dict(self):
        user = User("jane", "jane@mail.com", "manager")
        user.id = 10
        d = user.to_dict()
        assert d['id'] == 10
        assert d['role'] == "manager"