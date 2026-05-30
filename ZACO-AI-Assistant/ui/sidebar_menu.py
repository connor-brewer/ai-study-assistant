"""
Sidebar Menu - Navigation for the AI Companion app
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SidebarMenu(QWidget):
    # Signals for page navigation
    page_changed = pyqtSignal(str)
    
    def __init__(self, username, avatar_url=None):
        super().__init__()
        self.username = username
        self.avatar_url = avatar_url
        self.current_page = "dashboard"
        self.init_ui()
    
    def init_ui(self):
        """Initialize the sidebar UI"""
        self.setFixedWidth(240)
        self.setStyleSheet("""
            background-color: white;
            border-right: 1px solid #E5E7EB;
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo/Brand section
        brand_section = QWidget()
        brand_section.setFixedHeight(70)
        brand_section.setStyleSheet("background-color: white; border-bottom: 1px solid #E5E7EB;")
        brand_layout = QHBoxLayout(brand_section)
        brand_layout.setContentsMargins(24, 0, 24, 0)
        
        logo_label = QLabel("🦊 Deskling")
        logo_font = QFont("Segoe UI", 16, QFont.Bold)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #111827;")
        brand_layout.addWidget(logo_label)
        
        # Navigation buttons
        nav_section = QWidget()
        nav_layout = QVBoxLayout(nav_section)
        nav_layout.setContentsMargins(16, 20, 16, 20)
        nav_layout.setSpacing(4)
        
        # Dashboard button
        self.dashboard_btn = self.create_nav_button("Dashboard", "dashboard")
        self.dashboard_btn.clicked.connect(lambda: self.change_page("dashboard"))
        
        # Tasks button
        self.tasks_btn = self.create_nav_button("Tasks", "tasks")
        self.tasks_btn.clicked.connect(lambda: self.change_page("tasks"))
        
        # Focus Sessions button
        self.focus_btn = self.create_nav_button("Focus", "focus")
        self.focus_btn.clicked.connect(lambda: self.change_page("focus"))

        # Check In Session button
        self.checkin_btn = self.create_nav_button("Check-In", "checkin")
        self.checkin_btn.clicked.connect(lambda: self.change_page("checkin"))
        
        # Settings button
        self.settings_btn = self.create_nav_button("Settings", "settings")
        self.settings_btn.clicked.connect(lambda: self.change_page("settings"))
        
        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.tasks_btn)
        nav_layout.addWidget(self.focus_btn)
        nav_layout.addWidget(self.checkin_btn) #new
        nav_layout.addWidget(self.settings_btn)
        nav_layout.addStretch()
        
        # User profile section at bottom
        profile_section = QWidget()
        profile_section.setFixedHeight(70)
        profile_section.setStyleSheet("background-color: #F9FAFB; border-top: 1px solid #E5E7EB;")
        profile_layout = QHBoxLayout(profile_section)
        profile_layout.setContentsMargins(20, 16, 20, 16)
        
        profile_icon = QLabel("👤")
        profile_icon.setFixedSize(36, 36)
        profile_icon.setAlignment(Qt.AlignCenter)
        profile_icon.setStyleSheet("""
            background-color: #E5E7EB;
            border-radius: 18px;
            font-size: 16px;
        """)
        
        username_label = QLabel(self.username)
        username_font = QFont("Segoe UI", 13, QFont.Bold)
        username_label.setFont(username_font)
        username_label.setStyleSheet("color: #111827;")
        
        profile_layout.addWidget(profile_icon)
        profile_layout.addWidget(username_label)
        profile_layout.addStretch()
        
        # Add all sections
        layout.addWidget(brand_section)
        layout.addWidget(nav_section)
        layout.addWidget(profile_section)
        
        self.setLayout(layout)
        
        # Set initial active state
        self.set_active_button(self.dashboard_btn)
    
    def create_nav_button(self, text, page_id):
        """Create a navigation button"""
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty("page_id", page_id)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6B7280;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding-left: 16px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
                color: #111827;
            }
            QPushButton[active="true"] {
                background-color: #EEF2FF;
                color: #6366F1;
                font-weight: 600;
            }
        """)
        return btn
    



    def change_page(self, page_id):
        """Handle page change"""
        if page_id != self.current_page:
            self.current_page = page_id
            
            # Update button states
            for btn in [self.dashboard_btn, self.tasks_btn, self.focus_btn, self.checkin_btn,  self.settings_btn]:
                if btn.property("page_id") == page_id:
                    self.set_active_button(btn)
                else:
                    btn.setProperty("active", "false")
                    btn.setStyle(btn.style())
            
            # Emit signal
            self.page_changed.emit(page_id)
    
    def set_active_button(self, button):
        """Set a button as active"""
        button.setProperty("active", "true")
        button.setStyle(button.style())

