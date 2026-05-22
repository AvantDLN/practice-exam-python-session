from models.user import User

class UserController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db_manager.create_user_table()
    
    def add_user(self, username, email, role):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if role not in ['admin', 'manager', 'developer']:
            raise ValueError("Role must be admin, manager, or developer")
        
        user = User(username, email, role)
        return self.db_manager.add_user(user)
    
    def get_user(self, user_id):
        data = self.db_manager.get_user_by_id(user_id)
        if not data:
            return None
        user = User(data['username'], data['email'], data['role'])
        user.id = data['id']
        user.registration_date = data['registration_date']
        return user
    
    def get_all_users(self):
        users_data = self.db_manager.get_all_users()
        users = []
        for data in users_data:
            user = User(data['username'], data['email'], data['role'])
            user.id = data['id']
            user.registration_date = data['registration_date']
            users.append(user)
        return users
    
    def update_user(self, user_id, **kwargs):
        return self.db_manager.update_user(user_id, **kwargs)
    
    def delete_user(self, user_id):
        return self.db_manager.delete_user(user_id)
    
    def get_user_tasks(self, user_id, task_controller):
        return task_controller.get_tasks_by_user(user_id)