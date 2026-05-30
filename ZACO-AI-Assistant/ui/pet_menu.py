from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QInputDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from datetime import datetime

class PetMenu(QWidget):
    
    closed = pyqtSignal()
    
    def __init__(self, assistant, user_tasks=None, focus_page=None, overlay_window=None):
        super().__init__()
        self.assistant = assistant
        self.user_tasks = user_tasks or []
        self.focus_page = focus_page
        self.overlay_window = overlay_window
        self.timer_label = None
        self.init_ui()
        
        if self.focus_page and self.focus_page.timer_active:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.refresh_timer_display)
            self.update_timer.start(1000)  # Update every second
    
    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedWidth(340)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 30)  # Bottom margin for tail space
        main_layout.setSpacing(10)
        
        if self.focus_page and self.focus_page.timer_active:
            timer_frame = QFrame()
            timer_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 20px;
                }
            """)
            timer_layout = QVBoxLayout(timer_frame)
            timer_layout.setContentsMargins(24, 20, 24, 20)
            timer_layout.setSpacing(8)
            
            timer_title = QLabel("⏱️ Focus Timer")
            timer_title_font = QFont("Segoe UI", 13, QFont.Bold)
            timer_title.setFont(timer_title_font)
            timer_title.setStyleSheet("color: #6B7280;")
            
            time_str = self.focus_page.get_time_remaining_str() or "00:00"
            self.timer_label = QLabel(time_str)
            timer_display_font = QFont("Segoe UI", 36, QFont.Bold)
            self.timer_label.setFont(timer_display_font)
            self.timer_label.setStyleSheet("color: #6366F1;")
            self.timer_label.setAlignment(Qt.AlignCenter)
            
            timer_layout.addWidget(timer_title)
            timer_layout.addWidget(self.timer_label)
            
            main_layout.addWidget(timer_frame)
        
        chat_frame = QFrame()
        chat_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 20px;
            }
        """)
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(24, 20, 24, 20)
        chat_layout.setSpacing(0)
        
        message = self.assistant.get_interaction_message()
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_font = QFont("Segoe UI", 13)
        message_label.setFont(message_font)
        message_label.setStyleSheet("color: #1F2937; line-height: 1.6;")
        
        chat_layout.addWidget(message_label)
        
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 20px;
            }
        """)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(12, 12, 12, 12)
        actions_layout.setSpacing(10)
        
        chat_ai_btn = self.create_action_button(
            "💬",
            "Chat with AI",
            "Ask me anything!",
            "#10B981"
        )
        chat_ai_btn.clicked.connect(self.open_chat_dialog)
        actions_layout.addWidget(chat_ai_btn)
        
        upcoming_count = len([t for t in self.user_tasks if not t.get('completed')])
        tasks_subtitle = f"{upcoming_count} due soon" if upcoming_count > 0 else "Nothing due"
        self.tasks_btn = self.create_action_button(
            "📋", 
            "Tasks", 
            tasks_subtitle,
            "#6366F1"
        )
        self.tasks_btn.clicked.connect(self.open_tasks_page)
        actions_layout.addWidget(self.tasks_btn)
        
        main_layout.addWidget(chat_frame)
        main_layout.addWidget(actions_frame)
        
        self.setLayout(main_layout)
    
    def create_action_button(self, icon, title, subtitle, color):
        btn = QPushButton()
        btn.setFixedHeight(64)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #F9FAFB;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 14px 18px;
            }}
        """)
        
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(14)
        
        icon_label = QLabel(icon)
        icon_label.setFixedSize(36, 36)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            background-color: {color}20;
            border-radius: 18px;
            font-size: 18px;
        """)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 14, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #111827;")
        
        subtitle_label = QLabel(subtitle)
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6B7280;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)
        
        btn_layout.addWidget(icon_label)
        btn_layout.addLayout(text_layout)
        btn_layout.addStretch()
        
        return btn
    
    def open_chat_dialog(self):
        text, ok = QInputDialog.getText(
            self, 
            'Chat with AI Assistant', 
            'What would you like to ask?',
            text=""
        )
        
        if ok and text.strip():
            self.assistant.send_message_with_alert(text.strip(), self)
    
    def open_tasks_page(self):
        if self.overlay_window:
            self.close_menu()
            self.overlay_window.change_page("tasks")
            if not self.overlay_window.isVisible():
                self.overlay_window.show()
    
    def refresh_timer_display(self):
        if self.focus_page and self.focus_page.timer_active and self.timer_label:
            time_str = self.focus_page.get_time_remaining_str() or "00:00"
            self.timer_label.setText(time_str)
    
    def close_menu(self):
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        self.closed.emit()
        self.close()
    
    def update_position(self, avatar_pos):
        avatar_width = 100  # Width of compact avatar
        avatar_height = 100  # Height of compact avatar
        
        from PyQt5.QtWidgets import QDesktopWidget
        screen_geometry = QDesktopWidget().availableGeometry()
        
        menu_x = avatar_pos.x() + (avatar_width // 2) - self.width() - 40
        
        if menu_x < 10:
            menu_x = avatar_pos.x() + (avatar_width // 2) + 40
        
        if menu_x + self.width() > screen_geometry.width() - 10:
            menu_x = screen_geometry.width() - self.width() - 10
        
        menu_y = avatar_pos.y() - self.height() + 100
        
        if menu_y < 10:
            menu_y = avatar_pos.y() + avatar_height - 40
        
        self.move(menu_x, menu_y)

