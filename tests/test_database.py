import pytest
import tempfile
import os
from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from models.task import Task
from models.project import Project
from models.user import User

class TestDatabaseManager:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = DatabaseManager(self.temp_db.name)
    
    def teardown_method(self):
        self.db.close()
        os.unlink(self.temp_db.name)
    
    def test_create_task_table(self):
        self.db.create_task_table()
        self.db.connect()
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        assert cursor.fetchone() is not None
        self.db.close()
    
    def test_add_and_get_task(self):
        self.db.create_task_table()
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Test Task", "Desc", 1, due_date, 1, 1)
        task_id = self.db.add_task(task)
        
        fetched = self.db.get_task_by_id(task_id)
        assert fetched is not None
        assert fetched['title'] == "Test Task"
    
    def test_update_task(self):
        self.db.create_task_table()
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Original", "Desc", 2, due_date, 1, 1)
        task_id = self.db.add_task(task)
        
        self.db.update_task(task_id, title="Updated")
        updated = self.db.get_task_by_id(task_id)
        assert updated['title'] == "Updated"
    
    def test_delete_task(self):
        self.db.create_task_table()
        due_date = datetime.now() + timedelta(days=1)
        task = Task("To Delete", "Desc", 1, due_date, 1, 1)
        task_id = self.db.add_task(task)
        
        assert self.db.delete_task(task_id) == True
        assert self.db.get_task_by_id(task_id) is None
    
    def test_search_tasks(self):
        self.db.create_task_table()
        due_date = datetime.now() + timedelta(days=1)
        task1 = Task("Python Project", "Backend", 1, due_date, 1, 1)
        task2 = Task("Frontend Task", "React", 2, due_date, 1, 1)
        self.db.add_task(task1)
        self.db.add_task(task2)
        
        results = self.db.search_tasks("Python")
        assert len(results) == 1
        assert "Python" in results[0]['title']
    
    def test_create_project_table(self):
        self.db.create_project_table()
        self.db.connect()
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        assert cursor.fetchone() is not None
        self.db.close()
    
    def test_add_and_get_project(self):
        self.db.create_project_table()
        start = datetime.now()
        end = datetime.now() + timedelta(days=30)
        project = Project("Test Project", "Desc", start, end)
        proj_id = self.db.add_project(project)
        
        fetched = self.db.get_project_by_id(proj_id)
        assert fetched['name'] == "Test Project"
    
    def test_create_user_table(self):
        self.db.create_user_table()
        self.db.connect()
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
        self.db.close()
    
    def test_add_and_get_user(self):
        self.db.create_user_table()
        user = User("testuser", "test@mail.com", "developer")
        user_id = self.db.add_user(user)
        
        fetched = self.db.get_user_by_id(user_id)
        assert fetched['username'] == "testuser"