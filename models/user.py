from datetime import datetime

class User:
    def __init__(self, username, email, role):
        self.id = None
        self.username = username
        self.email = email
        self.role = role
        self.registration_date = datetime.now()
    
    def update_info(self, username=None, email=None, role=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if role:
            self.role = role
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'registration_date': self.registration_date.isoformat()
        }