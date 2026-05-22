import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='database/tasks.db'):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_tables(self):
    self.create_task_table()
    self.create_project_table()
    self.create_user_table()
    
    def create_task_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                due_date TEXT NOT NULL,
                project_id INTEGER NOT NULL,
                assignee_id INTEGER NOT NULL
            )
        ''')
        conn.commit()
        self.close()
    
    def add_task(self, task):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task.title, task.description, task.priority, task.status, 
              task.due_date.isoformat(), task.project_id, task.assignee_id))
        conn.commit()
        task.id = cursor.lastrowid
        self.close()
        return task.id
    
    def get_task_by_id(self, task_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        self.close()
        return dict(row) if row else None
    
    def get_all_tasks(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def update_task(self, task_id, **kwargs):
        conn = self.connect()
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            if key == 'due_date' and value:
                value = value.isoformat()
            fields.append(f"{key} = ?")
            values.append(value)
        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        self.close()
        return cursor.rowcount > 0
    
    def delete_task(self, task_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        self.close()
        return cursor.rowcount > 0
    
    def search_tasks(self, query):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE title LIKE ? OR description LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def get_tasks_by_project(self, project_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def get_tasks_by_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE assignee_id = ?', (user_id,))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def create_project_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active'
            )
        ''')
        conn.commit()
        self.close()
    
    def add_project(self, project):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (project.name, project.description, project.start_date.isoformat(),
              project.end_date.isoformat(), project.status))
        conn.commit()
        project.id = cursor.lastrowid
        self.close()
        return project.id
    
    def get_project_by_id(self, project_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        self.close()
        return dict(row) if row else None
    
    def get_all_projects(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects')
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def update_project(self, project_id, **kwargs):
        conn = self.connect()
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['start_date', 'end_date'] and value:
                value = value.isoformat()
            fields.append(f"{key} = ?")
            values.append(value)
        values.append(project_id)
        query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        self.close()
        return cursor.rowcount > 0
    
    def delete_project(self, project_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        conn.commit()
        self.close()
        return cursor.rowcount > 0
    
    def create_user_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        ''')
        conn.commit()
        self.close()
    
    def add_user(self, user):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, role, registration_date)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.email, user.role, user.registration_date.isoformat()))
        conn.commit()
        user.id = cursor.lastrowid
        self.close()
        return user.id
    
    def get_user_by_id(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        self.close()
        return dict(row) if row else None
    
    def get_all_users(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def update_user(self, user_id, **kwargs):
        conn = self.connect()
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            if value:
                fields.append(f"{key} = ?")
                values.append(value)
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        self.close()
        return cursor.rowcount > 0
    
    def delete_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        self.close()
        return cursor.rowcount > 0

