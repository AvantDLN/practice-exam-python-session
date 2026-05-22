from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date):
        self.id = None
        self.name = name
        self.description = description
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.fromisoformat(start_date)
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.fromisoformat(end_date)
        self.status = 'active'
    
    def update_status(self, new_status):
        valid_statuses = ['active', 'completed', 'on_hold']
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False
    
    def get_progress(self, db_manager):
        tasks = db_manager.get_tasks_by_project(self.id)
        if not tasks:
            return 0
        completed = sum(1 for t in tasks if t['status'] == 'completed')
        return int((completed / len(tasks)) * 100)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status
        }