import pytest
import tempfile
import os
from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController

class TestTaskController:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = DatabaseManager(self.temp_db.name)
        self.controller = TaskController(self.db)
    
    def teardown_method(self):
        self.db.close()
        os.unlink(self.temp_db.name)
    
    def test_add_task(self):
        due_date = (datetime.now() + timedelta(days=1)).isoformat()
        task_id = self.controller.add_task("Test", "Desc", 1, due_date, 1, 1)
        assert task_id is not None
    
    def test_get_task(self):
        due_date = (datetime.now() + timedelta(days=1)).isoformat()
        task_id = self.controller.add_task("Get Test", "Desc", 2, due_date, 1, 1)
        task = self.controller.get_task(task_id)
        assert task.title == "Get Test"
    
    def test_update_task_status(self):
        due_date = (datetime.now() + timedelta(days=1)).isoformat()
        task_id = self.controller.add_task("Status Test", "Desc", 1, due_date, 1, 1)
        assert self.controller.update_task_status(task_id, "in_progress") == True
        task = self.controller.get_task(task_id)
        assert task.status == "in_progress"
    
    def test_get_overdue_tasks(self):
        past_date = (datetime.now() - timedelta(days=1)).isoformat()
        future_date = (datetime.now() + timedelta(days=1)).isoformat()
        self.controller.add_task("Overdue", "Desc", 1, past_date, 1, 1)
        self.controller.add_task("Not Overdue", "Desc", 1, future_date, 1, 1)
        overdue = self.controller.get_overdue_tasks()
        assert len(overdue) == 1
        assert overdue[0].title == "Overdue"
    
    def test_delete_task(self):
        due_date = (datetime.now() + timedelta(days=1)).isoformat()
        task_id = self.controller.add_task("Delete Me", "Desc", 1, due_date, 1, 1)
        assert self.controller.delete_task(task_id) == True
        assert self.controller.get_task(task_id) is None

class TestProjectController:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = DatabaseManager(self.temp_db.name)
        self.controller = ProjectController(self.db)
        self.task_controller = TaskController(self.db)
    
    def teardown_method(self):
        self.db.close()
        os.unlink(self.temp_db.name)
    
    def test_add_project(self):
        start = datetime.now().isoformat()
        end = (datetime.now() + timedelta(days=30)).isoformat()
        proj_id = self.controller.add_project("New Project", "Desc", start, end)
        assert proj_id is not None
    
    def test_get_project(self):
        start = datetime.now().isoformat()
        end = (datetime.now() + timedelta(days=30)).isoformat()
        proj_id = self.controller.add_project("Get Project", "Desc", start, end)
        project = self.controller.get_project(proj_id)
        assert project.name == "Get Project"
    
    def test_update_project_status(self):
        start = datetime.now().isoformat()
        end = (datetime.now() + timedelta(days=30)).isoformat()
        proj_id = self.controller.add_project("Status Proj", "Desc", start, end)
        assert self.controller.update_project_status(proj_id, "on_hold") == True
        project = self.controller.get_project(proj_id)
        assert project.status == "on_hold"

class TestUserController:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = DatabaseManager(self.temp_db.name)
        self.controller = UserController(self.db)
    
    def teardown_method(self):
        self.db.close()
        os.unlink(self.temp_db.name)
    
    def test_add_user(self):
        user_id = self.controller.add_user("testuser", "test@mail.com", "developer")
        assert user_id is not None
    
    def test_get_user(self):
        user_id = self.controller.add_user("john", "john@mail.com", "manager")
        user = self.controller.get_user(user_id)
        assert user.username == "john"
    
    def test_update_user(self):
        user_id = self.controller.add_user("oldname", "old@mail.com", "developer")
        assert self.controller.update_user(user_id, username="newname") == True
        user = self.controller.get_user(user_id)
        assert user.username == "newname"
    
    def test_delete_user(self):
        user_id = self.controller.add_user("deleteuser", "delete@mail.com", "developer")
        assert self.controller.delete_user(user_id) == True
        assert self.controller.get_user(user_id) is None