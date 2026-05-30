"""
Tasks Page - Calendar-style to-do list management
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QScrollArea, QFrame, 
                             QCheckBox, QComboBox, QTextEdit, QDateEdit, QDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime

class AddTaskDialog(QDialog):
    """Dialog for adding a new task with details"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #F3F4F6;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)
        
        # Title
        title_label = QLabel("Title")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet("color: #111827;")
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("What needs to be done?")
        self.title_input.setMinimumHeight(40)
        self.title_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #1F2937;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """)
        
        # Description
        desc_label = QLabel("Description (optional)")
        desc_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        desc_label.setStyleSheet("color: #111827;")
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Add more details...")
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #1F2937;
            }
            QTextEdit:focus {
                border: 1px solid #6366F1;
            }
        """)
        
        # Due date and priority row
        details_layout = QHBoxLayout()
        details_layout.setSpacing(12)
        
        # Due date
        date_container = QWidget()
        date_layout = QVBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(6)
        
        date_label = QLabel("Due Date")
        date_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        date_label.setStyleSheet("color: #111827;")
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumHeight(40)
        self.date_input.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #1F2937;
            }
            QDateEdit:focus {
                border: 1px solid #6366F1;
            }
            QDateEdit::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        
        # Priority
        priority_container = QWidget()
        priority_layout = QVBoxLayout(priority_container)
        priority_layout.setContentsMargins(0, 0, 0, 0)
        priority_layout.setSpacing(6)
        
        priority_label = QLabel("Priority")
        priority_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        priority_label.setStyleSheet("color: #111827;")
        
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.priority_input.setCurrentIndex(1)  # Default to Medium
        self.priority_input.setMinimumHeight(40)
        self.priority_input.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #1F2937;
            }
            QComboBox:focus {
                border: 1px solid #6366F1;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
        
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_input)
        
        details_layout.addWidget(date_container)
        details_layout.addWidget(priority_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(44)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6B7280;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        add_btn = QPushButton("Add Task")
        add_btn.setMinimumHeight(44)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        add_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_btn)
        
        # Add all widgets
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)
        layout.addLayout(details_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_task_data(self):
        """Return the task data"""
        return {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip(),
            'due_date': self.date_input.date().toPyDate().isoformat(),
            'priority': self.priority_input.currentText().lower()
        }


class TasksPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.user_id = user_data.get('id')
        self.db = db
        self.tasks = []
        self.init_ui()
        self.load_tasks()
    
    def init_ui(self):
        """Initialize the tasks UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        header_label = QLabel("My Tasks")
        header_font = QFont("Segoe UI", 26, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #111827;")
        
        add_btn = QPushButton("+ New Task")
        add_btn.setFixedHeight(44)
        add_btn.setFixedWidth(130)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        add_btn.clicked.connect(self.show_add_dialog)
        
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        
        subtitle_label = QLabel("Stay organized and get things done")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6B7280;")
        
        # Tasks scroll area
        self.tasks_scroll = QScrollArea()
        self.tasks_scroll.setWidgetResizable(True)
        self.tasks_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tasks_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setSpacing(12)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        
        self.tasks_scroll.setWidget(self.tasks_container)
        
        # Add widgets
        layout.addLayout(header_layout)
        layout.addWidget(subtitle_label)
        layout.addSpacing(16)
        layout.addWidget(self.tasks_scroll)
        
        self.setLayout(layout)
    
    def show_add_dialog(self):
        """Show the add task dialog"""
        dialog = AddTaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            if task_data['title']:
                self.add_task(task_data)
    
    def load_tasks(self):
        """Load tasks from database"""
        if self.db.is_connected():
            try:
                # Try multiple methods to get the authenticated user ID
                auth_user_id = None
                
                # Method 1: Get from session
                try:
                    session = self.db.get_session()
                    if session and hasattr(session, 'user') and session.user:
                        auth_user_id = session.user.id
                        print(f"Got user ID from session: {auth_user_id}")
                except Exception as e:
                    print(f"Session method failed: {e}")
                
                # Method 2: Get directly from auth
                if not auth_user_id:
                    try:
                        user_response = self.db.client.auth.get_user()
                        if user_response and hasattr(user_response, 'user') and user_response.user:
                            auth_user_id = user_response.user.id
                            print(f"Got user ID from get_user: {auth_user_id}")
                    except Exception as e:
                        print(f"get_user method failed: {e}")
                
                # Method 3: Use user_id from user_data (should match auth.users.id)
                if not auth_user_id and self.user_id:
                    auth_user_id = self.user_id
                    print(f"Using user_id from user_data: {auth_user_id}")
                
                # Load tasks if we have a user ID
                if auth_user_id:
                    print(f"Loading tasks for user: {auth_user_id}")
                    result = self.db.client.table('tasks').select('*').eq('user_id', auth_user_id).order('due_date', desc=False).execute()
                    print(f"Tasks query result: {len(result.data) if result.data else 0} tasks found")
                    if result.data:
                        self.tasks = result.data
                        self.render_tasks()
                    else:
                        print("No tasks found in database")
                        self.tasks = []
                        self.render_tasks()
                else:
                    print("Could not determine user ID - cannot load tasks")
            except Exception as e:
                print(f"Error loading tasks: {e}")
                import traceback
                traceback.print_exc()
    
    def render_tasks(self):
        """Render tasks to UI"""
        # Clear existing tasks
        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add tasks
        for task in self.tasks:
            task_widget = self.create_task_widget(task)
            self.tasks_layout.addWidget(task_widget)
    
    def create_task_widget(self, task):
        """Create a calendar-style task widget"""
        task_frame = QFrame()
        task_frame.setMinimumHeight(90)
        
        # Priority colors
        priority_colors = {
            'high': '#EF4444',
            'medium': '#F59E0B',
            'low': '#10B981'
        }
        priority = task.get('priority', 'medium')
        priority_color = priority_colors.get(priority, '#F59E0B')
        
        task_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 4px solid {priority_color};
                border-radius: 12px;
                padding: 0px;
            }}
        """)
        
        frame_layout = QHBoxLayout(task_frame)
        frame_layout.setContentsMargins(20, 16, 20, 16)
        frame_layout.setSpacing(16)
        
        # Checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(task.get('completed', False))
        checkbox.setFixedSize(24, 24)
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 6px;
                border: 2px solid #D1D5DB;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #6366F1;
                border: 2px solid #6366F1;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #6366F1;
            }
        """)
        checkbox.stateChanged.connect(lambda state, t=task: self.toggle_task(t, state))
        
        # Content layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(6)
        
        # Title
        task_title = QLabel(task.get('title', ''))
        task_font = QFont("Segoe UI", 15, QFont.Bold)
        task_title.setFont(task_font)
        task_title.setStyleSheet(f"""
            color: {'#9CA3AF' if task.get('completed') else '#111827'};
            text-decoration: {'line-through' if task.get('completed') else 'none'};
        """)
        
        # Description (if exists)
        description = task.get('description')
        if description:
            task_desc = QLabel(description)
            desc_font = QFont("Segoe UI", 12)
            task_desc.setFont(desc_font)
            task_desc.setWordWrap(True)
            task_desc.setStyleSheet("color: #6B7280;")
            task_desc.setMaximumHeight(40)
        
        # Due date and priority
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(16)
        
        due_date = task.get('due_date')
        if due_date:
            try:
                date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                date_str = date_obj.strftime("%b %d, %Y")
                
                # Check if overdue
                is_overdue = date_obj.date() < datetime.now().date() and not task.get('completed')
                
                due_label = QLabel(f"📅 {date_str}")
                due_font = QFont("Segoe UI", 11)
                due_label.setFont(due_font)
                due_label.setStyleSheet(f"color: {'#EF4444' if is_overdue else '#6B7280'}; font-weight: 500;")
                meta_layout.addWidget(due_label)
            except:
                pass
        
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        priority_label = QLabel(f"{priority_emoji.get(priority, '🟡')} {priority.capitalize()}")
        priority_font = QFont("Segoe UI", 11)
        priority_label.setFont(priority_font)
        priority_label.setStyleSheet("color: #6B7280; font-weight: 500;")
        meta_layout.addWidget(priority_label)
        meta_layout.addStretch()
        
        content_layout.addWidget(task_title)
        if description:
            content_layout.addWidget(task_desc)
        content_layout.addLayout(meta_layout)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(40, 40)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FEE2E2;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_task(task))
        
        frame_layout.addWidget(checkbox)
        frame_layout.addLayout(content_layout, 1)
        frame_layout.addWidget(delete_btn)
        
        return task_frame
    
    def add_task(self, task_data):
        """Add a new task"""
        if self.db.is_connected():
            try:
                # Get the authenticated user's ID from Supabase auth
                session = self.db.get_session()
                if session and hasattr(session, 'user') and session.user:
                    auth_user_id = session.user.id
                else:
                    # Fallback: try to get user directly
                    user = self.db.client.auth.get_user()
                    if user and hasattr(user, 'user') and user.user:
                        auth_user_id = user.user.id
                    else:
                        print("No active session found - cannot add task")
                        return
                
                result = self.db.client.table('tasks').insert({
                    'user_id': auth_user_id,
                    'title': task_data['title'],
                    'description': task_data.get('description'),
                    'due_date': task_data.get('due_date'),
                    'priority': task_data.get('priority', 'medium'),
                    'completed': False
                }).execute()
                
                if result.data:
                    self.tasks.insert(0, result.data[0])
                    self.render_tasks()
            except Exception as e:
                print(f"Error adding task: {e}")
    
    def toggle_task(self, task, state):
        """Toggle task completion"""
        if self.db.is_connected():
            try:
                completed = (state == Qt.Checked)
                self.db.client.table('tasks').update({
                    'completed': completed
                }).eq('id', task['id']).execute()
                
                task['completed'] = completed
                self.render_tasks()
            except Exception as e:
                print(f"Error toggling task: {e}")
    
    def delete_task(self, task):
        """Delete a task"""
        if self.db.is_connected():
            try:
                self.db.client.table('tasks').delete().eq('id', task['id']).execute()
                self.tasks.remove(task)
                self.render_tasks()
            except Exception as e:
                print(f"Error deleting task: {e}")
