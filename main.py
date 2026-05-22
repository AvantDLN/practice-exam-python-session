import tkinter as tk
from tkinter import ttk, messagebox
from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("900x600")
        
        self.db = DatabaseManager()
        self.task_controller = TaskController(self.db)
        self.project_controller = ProjectController(self.db)
        self.user_controller = UserController(self.db)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tasks_frame = ttk.Frame(self.notebook)
        self.projects_frame = ttk.Frame(self.notebook)
        self.users_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tasks_frame, text="Tasks")
        self.notebook.add(self.projects_frame, text="Projects")
        self.notebook.add(self.users_frame, text="Users")
        
        self.setup_tasks_view()
        self.setup_projects_view()
        self.setup_users_view()
        
        self.refresh_tasks()
        self.refresh_projects()
        self.refresh_users()
    
    def setup_tasks_view(self):
        form_frame = ttk.LabelFrame(self.tasks_frame, text="Add/Edit Task")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=2)
        self.task_title = ttk.Entry(form_frame, width=30)
        self.task_title.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=2)
        self.task_desc = ttk.Entry(form_frame, width=30)
        self.task_desc.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Priority (1-3):").grid(row=2, column=0, padx=5, pady=2)
        self.task_priority = ttk.Combobox(form_frame, values=[1, 2, 3], width=28)
        self.task_priority.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=2)
        self.task_due = ttk.Entry(form_frame, width=30)
        self.task_due.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Project ID:").grid(row=4, column=0, padx=5, pady=2)
        self.task_project = ttk.Entry(form_frame, width=30)
        self.task_project.grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Assignee ID:").grid(row=5, column=0, padx=5, pady=2)
        self.task_assignee = ttk.Entry(form_frame, width=30)
        self.task_assignee.grid(row=5, column=1, padx=5, pady=2)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.LabelFrame(self.tasks_frame, text="Task List")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Title", "Priority", "Status", "Due Date")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.task_tree.heading(col, text=col)
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        
        btn_frame2 = ttk.Frame(list_frame)
        btn_frame2.pack(pady=5)
        ttk.Button(btn_frame2, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame2, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
    
    def setup_projects_view(self):
        form_frame = ttk.LabelFrame(self.projects_frame, text="Add Project")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2)
        self.proj_name = ttk.Entry(form_frame, width=30)
        self.proj_name.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=2)
        self.proj_desc = ttk.Entry(form_frame, width=30)
        self.proj_desc.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Start Date:").grid(row=2, column=0, padx=5, pady=2)
        self.proj_start = ttk.Entry(form_frame, width=30)
        self.proj_start.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="End Date:").grid(row=3, column=0, padx=5, pady=2)
        self.proj_end = ttk.Entry(form_frame, width=30)
        self.proj_end.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Button(form_frame, text="Add Project", command=self.add_project).grid(row=4, column=0, columnspan=2, pady=10)
        
        list_frame = ttk.LabelFrame(self.projects_frame, text="Projects")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Name", "Status", "Progress")
        self.proj_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.proj_tree.heading(col, text=col)
        self.proj_tree.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Complete Project", command=self.complete_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Project", command=self.delete_project).pack(side=tk.LEFT, padx=5)
    
    def setup_users_view(self):
        form_frame = ttk.LabelFrame(self.users_frame, text="Add User")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=2)
        self.user_name = ttk.Entry(form_frame, width=30)
        self.user_name.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=2)
        self.user_email = ttk.Entry(form_frame, width=30)
        self.user_email.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, padx=5, pady=2)
        self.user_role = ttk.Combobox(form_frame, values=['admin', 'manager', 'developer'], width=28)
        self.user_role.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Button(form_frame, text="Add User", command=self.add_user).grid(row=3, column=0, columnspan=2, pady=10)
        
        list_frame = ttk.LabelFrame(self.users_frame, text="Users")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Username", "Email", "Role")
        self.user_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.user_tree.heading(col, text=col)
        self.user_tree.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        try:
            self.task_controller.add_task(
                self.task_title.get(),
                self.task_desc.get(),
                int(self.task_priority.get()),
                self.task_due.get(),
                int(self.task_project.get()),
                int(self.task_assignee.get())
            )
            self.refresh_tasks()
            self.clear_task_form()
            messagebox.showinfo("Success", "Task added")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def complete_task(self):
        selected = self.task_tree.selection()
        if selected:
            task_id = self.task_tree.item(selected[0])['values'][0]
            self.task_controller.update_task_status(task_id, "completed")
            self.refresh_tasks()
    
    def delete_task(self):
        selected = self.task_tree.selection()
        if selected:
            task_id = self.task_tree.item(selected[0])['values'][0]
            self.task_controller.delete_task(task_id)
            self.refresh_tasks()
    
    def refresh_tasks(self):
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
        for task in self.task_controller.get_all_tasks():
            self.task_tree.insert("", tk.END, values=(
                task.id, task.title, task.priority, task.status, task.due_date.date()
            ))
    
    def clear_task_form(self):
        self.task_title.delete(0, tk.END)
        self.task_desc.delete(0, tk.END)
        self.task_priority.set('')
        self.task_due.delete(0, tk.END)
        self.task_project.delete(0, tk.END)
        self.task_assignee.delete(0, tk.END)
    
    def add_project(self):
        try:
            self.project_controller.add_project(
                self.proj_name.get(),
                self.proj_desc.get(),
                self.proj_start.get(),
                self.proj_end.get()
            )
            self.refresh_projects()
            self.clear_project_form()
            messagebox.showinfo("Success", "Project added")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def complete_project(self):
        selected = self.proj_tree.selection()
        if selected:
            proj_id = self.proj_tree.item(selected[0])['values'][0]
            self.project_controller.update_project_status(proj_id, "completed")
            self.refresh_projects()
    
    def delete_project(self):
        selected = self.proj_tree.selection()
        if selected:
            proj_id = self.proj_tree.item(selected[0])['values'][0]
            self.project_controller.delete_project(proj_id)
            self.refresh_projects()
    
    def refresh_projects(self):
        for row in self.proj_tree.get_children():
            self.proj_tree.delete(row)
        for proj in self.project_controller.get_all_projects():
            progress = self.project_controller.get_project_progress(proj.id)
            self.proj_tree.insert("", tk.END, values=(proj.id, proj.name, proj.status, f"{progress}%"))
    
    def clear_project_form(self):
        self.proj_name.delete(0, tk.END)
        self.proj_desc.delete(0, tk.END)
        self.proj_start.delete(0, tk.END)
        self.proj_end.delete(0, tk.END)
    
    def add_user(self):
        try:
            self.user_controller.add_user(
                self.user_name.get(),
                self.user_email.get(),
                self.user_role.get()
            )
            self.refresh_users()
            self.clear_user_form()
            messagebox.showinfo("Success", "User added")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_user(self):
        selected = self.user_tree.selection()
        if selected:
            user_id = self.user_tree.item(selected[0])['values'][0]
            self.user_controller.delete_user(user_id)
            self.refresh_users()
    
    def refresh_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for user in self.user_controller.get_all_users():
            self.user_tree.insert("", tk.END, values=(user.id, user.username, user.email, user.role))
    
    def clear_user_form(self):
        self.user_name.delete(0, tk.END)
        self.user_email.delete(0, tk.END)
        self.user_role.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()