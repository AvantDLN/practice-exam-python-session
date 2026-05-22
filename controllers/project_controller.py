from datetime import datetime
from models.project import Project

class ProjectController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db_manager.create_project_table()
    
    def add_project(self, name, description, start_date, end_date):
        if not name:
            raise ValueError("Name is required")
        start_obj = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
        end_obj = datetime.fromisoformat(end_date) if isinstance(end_date, str) else end_date
        if start_obj > end_obj:
            raise ValueError("Start date must be before end date")
        
        project = Project(name, description, start_obj, end_obj)
        return self.db_manager.add_project(project)
    
    def get_project(self, project_id):
        data = self.db_manager.get_project_by_id(project_id)
        if not data:
            return None
        project = Project(data['name'], data['description'], data['start_date'], data['end_date'])
        project.id = data['id']
        project.status = data['status']
        return project
    
    def get_all_projects(self):
        projects_data = self.db_manager.get_all_projects()
        projects = []
        for data in projects_data:
            project = Project(data['name'], data['description'], data['start_date'], data['end_date'])
            project.id = data['id']
            project.status = data['status']
            projects.append(project)
        return projects
    
    def update_project(self, project_id, **kwargs):
        return self.db_manager.update_project(project_id, **kwargs)
    
    def delete_project(self, project_id):
        return self.db_manager.delete_project(project_id)
    
    def update_project_status(self, project_id, new_status):
        project = self.get_project(project_id)
        if project and project.update_status(new_status):
            return self.db_manager.update_project(project_id, status=new_status)
        return False
    
    def get_project_progress(self, project_id):
        project = self.get_project(project_id)
        if not project:
            return 0
        return project.get_progress(self.db_manager)