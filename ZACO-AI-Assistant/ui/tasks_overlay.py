"""
Tasks Overlay - Quick view of upcoming tasks
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class TasksOverlay(QWidget):
    """Overlay showing upcoming tasks"""
    
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.init_ui()
    
    def init_ui(self):
        """Initialize the overlay UI"""
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setFixedSize(400, 500)
        
        # Center on screen
        from PyQt5.QtWidgets import QDesktopWidget
        screen_geometry = QDesktopWidget().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 20px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(16)
        
        # Header
        header_label = QLabel("📋 Upcoming Tasks")
        header_font = QFont("Segoe UI", 20, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #111827;")
        
        subtitle = QLabel(f"{len(self.tasks)} task{'s' if len(self.tasks) != 1 else ''} due soon")
        subtitle_font = QFont("Segoe UI", 13)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #6B7280;")
        
        # Tasks scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        tasks_container = QWidget()
        tasks_layout = QVBoxLayout(tasks_container)
        tasks_layout.setSpacing(12)
        tasks_layout.setAlignment(Qt.AlignTop)
        
        if self.tasks:
            for task in self.tasks:
                task_widget = self.create_task_widget(task)
                tasks_layout.addWidget(task_widget)
        else:
            no_tasks = QLabel("No tasks due in the next 7 days! 🎉")
            no_tasks.setAlignment(Qt.AlignCenter)
            no_tasks_font = QFont("Segoe UI", 13)
            no_tasks.setFont(no_tasks_font)
            no_tasks.setStyleSheet("color: #6B7280; padding: 40px;")
            tasks_layout.addWidget(no_tasks)
        
        scroll.setWidget(tasks_container)
        
        container_layout.addWidget(header_label)
        container_layout.addWidget(subtitle)
        container_layout.addSpacing(8)
        container_layout.addWidget(scroll)
        
        layout.addWidget(container)
        self.setLayout(layout)
    
    def create_task_widget(self, task):
        """Create a task widget"""
        frame = QFrame()
        frame.setFixedHeight(70)
        
        priority_colors = {
            'high': '#EF4444',
            'medium': '#F59E0B',
            'low': '#10B981'
        }
        priority = task.get('priority', 'medium')
        color = priority_colors.get(priority, '#F59E0B')
        
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: #F9FAFB;
                border-left: 4px solid {color};
                border-radius: 10px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        # Title
        title = QLabel(task.get('title', ''))
        title_font = QFont("Segoe UI", 13, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #111827;")
        
        # Due date
        due_date_str = ""
        due_date = task.get('due_date')
        if due_date:
            try:
                date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                now = datetime.now()
                days_until = (date_obj.date() - now.date()).days
                
                if days_until == 0:
                    due_date_str = "📅 Due today"
                elif days_until == 1:
                    due_date_str = "📅 Due tomorrow"
                elif days_until < 0:
                    due_date_str = f"⚠️ Overdue by {abs(days_until)} day{'s' if abs(days_until) != 1 else ''}"
                else:
                    due_date_str = f"📅 Due in {days_until} days"
            except:
                pass
        
        due_label = QLabel(due_date_str)
        due_font = QFont("Segoe UI", 11)
        due_label.setFont(due_font)
        due_label.setStyleSheet("color: #6B7280;")
        
        layout.addWidget(title)
        layout.addWidget(due_label)
        
        return frame
    
    def mousePressEvent(self, event):
        """Close on click outside"""
        self.close()

