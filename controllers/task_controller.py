from datetime import datetime
from models.task import Task

class TaskController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db_manager.create_task_table()
    
    def add_task(self, title, description, priority, due_date, project_id, assignee_id):
        if not title:
            raise ValueError("Title is required")
        if priority not in [1, 2, 3]:
            raise ValueError("Priority must be 1, 2, or 3")
        
        due_date_obj = datetime.fromisoformat(due_date) if isinstance(due_date, str) else due_date
        task = Task(title, description, priority, due_date_obj, project_id, assignee_id)
        return self.db_manager.add_task(task)
    
    def get_task(self, task_id):
        data = self.db_manager.get_task_by_id(task_id)
        if not data:
            return None
        task = Task(data['title'], data['description'], data['priority'], 
                    data['due_date'], data['project_id'], data['assignee_id'])
        task.id = data['id']
        task.status = data['status']
        return task
    
    def get_all_tasks(self):
        tasks_data = self.db_manager.get_all_tasks()
        tasks = []
        for data in tasks_data:
            task = Task(data['title'], data['description'], data['priority'],
                       data['due_date'], data['project_id'], data['assignee_id'])
            task.id = data['id']
            task.status = data['status']
            tasks.append(task)
        return tasks
    
    def update_task(self, task_id, **kwargs):
        return self.db_manager.update_task(task_id, **kwargs)
    
    def delete_task(self, task_id):
        return self.db_manager.delete_task(task_id)
    
    def search_tasks(self, query):
        tasks_data = self.db_manager.search_tasks(query)
        tasks = []
        for data in tasks_data:
            task = Task(data['title'], data['description'], data['priority'],
                       data['due_date'], data['project_id'], data['assignee_id'])
            task.id = data['id']
            task.status = data['status']
            tasks.append(task)
        return tasks
    
    def update_task_status(self, task_id, new_status):
        task = self.get_task(task_id)
        if task and task.update_status(new_status):
            return self.db_manager.update_task(task_id, status=new_status)
        return False
    
    def get_overdue_tasks(self):
        all_tasks = self.get_all_tasks()
        return [t for t in all_tasks if t.is_overdue()]
    
    def get_tasks_by_project(self, project_id):
        tasks_data = self.db_manager.get_tasks_by_project(project_id)
        tasks = []
        for data in tasks_data:
            task = Task(data['title'], data['description'], data['priority'],
                       data['due_date'], data['project_id'], data['assignee_id'])
            task.id = data['id']
            task.status = data['status']
            tasks.append(task)
        return tasks
    
    def get_tasks_by_user(self, user_id):
        tasks_data = self.db_manager.get_tasks_by_user(user_id)
        tasks = []
        for data in tasks_data:
            task = Task(data['title'], data['description'], data['priority'],
                       data['due_date'], data['project_id'], data['assignee_id'])
            task.id = data['id']
            task.status = data['status']
            tasks.append(task)
        return tasks