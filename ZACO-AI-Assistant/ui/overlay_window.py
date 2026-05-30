from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QSystemTrayIcon, 
                             QMenu, QAction, QStackedWidget, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QIcon, QPixmap
from assistant.ai_assistant import AIAssistant
from ui.sidebar_menu import SidebarMenu
from ui.pages.dashboard_page import DashboardPage
from ui.pages.tasks_page import TasksPage
from ui.pages.focus_page import FocusPage
from ui.pages.checkin_page import CheckinPage
from ui.pages.settings_page import SettingsPage
from database.supabase_client import get_supabase_client
from utils.session_manager import get_session_manager
from datetime import datetime

class OverlayWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        if isinstance(user_data, dict):
            self.user_data = user_data
            self.username = user_data.get('username', 'User')
            self.user_id = user_data.get('id')
            self.avatar_url = user_data.get('avatar_url')
        else:
            self.username = user_data
            self.user_data = {'username': user_data, 'id': None}
            self.user_id = None
            self.avatar_url = None
        
        self.assistant = AIAssistant(self.username)
        self.is_active = False
        self.dragging = False
        self.offset = QPoint()
        self.is_maximized = False
        self.normal_geometry = None
        self.is_quitting = False  # Track if we're actually quitting vs hiding to tray
        self.is_logging_out = False  # Track if we're logging out
        
        self.db = get_supabase_client()
        self.session_manager = get_session_manager()
        self.current_session_id = None
        self.session_start_time = None
        
        self.init_ui()
        self.setup_timer()
        self.setup_system_tray()
    
    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setMinimumSize(900, 600)
        self.resize(1200, 750)
        
        self.center_window()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = self.create_title_bar()
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.sidebar = SidebarMenu(self.username, self.avatar_url)
        self.sidebar.page_changed.connect(self.change_page)
        
        from PyQt5.QtWidgets import QScrollArea
        
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background-color: #F9FAFB;")
        
        self.dashboard_page = DashboardPage(self.user_data)
        self.tasks_page = TasksPage(self.user_data, self.db)
        self.focus_page = FocusPage(self.user_data)
        self.checkin_page = CheckinPage(self.user_data)
        self.settings_page = SettingsPage(self.user_data, self.db)
        
        self.dashboard_page.toggle_button.clicked.connect(self.toggle_assistant)
        
        self.dashboard_scroll = QScrollArea()
        self.dashboard_scroll.setWidget(self.dashboard_page)
        self.dashboard_scroll.setWidgetResizable(True)
        self.dashboard_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dashboard_scroll.setStyleSheet("QScrollArea { background-color: #F9FAFB; border: none; }")
        
        self.tasks_scroll = QScrollArea()
        self.tasks_scroll.setWidget(self.tasks_page)
        self.tasks_scroll.setWidgetResizable(True)
        self.tasks_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tasks_scroll.setStyleSheet("QScrollArea { background-color: #F9FAFB; border: none; }")
        
        self.focus_scroll = QScrollArea()
        self.focus_scroll.setWidget(self.focus_page)
        self.focus_scroll.setWidgetResizable(True)
        self.focus_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.focus_scroll.setStyleSheet("QScrollArea { background-color: #F9FAFB; border: none; }")
        
        self.settings_scroll = QScrollArea()
        self.settings_scroll.setWidget(self.settings_page)
        self.settings_scroll.setWidgetResizable(True)
        self.settings_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.settings_scroll.setStyleSheet("QScrollArea { background-color: #F9FAFB; border: none; }")
        
        self.pages.addWidget(self.dashboard_scroll)
        self.pages.addWidget(self.tasks_scroll)
        self.pages.addWidget(self.focus_scroll)

        self.checkin_scroll = QScrollArea()
        self.checkin_scroll.setWidget(self.checkin_page)
        self.checkin_scroll.setWidgetResizable(True)
        self.checkin_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.checkin_scroll.setStyleSheet("QScrollArea { background-color: #F9FAFB; border: none; }")
        self.pages.addWidget(self.checkin_scroll)
        self.pages.addWidget(self.settings_scroll)
        
        self.pages.setCurrentIndex(0)
        
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages)
        
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_widget)
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #F7F8FA;
                color: #1F2937;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    def create_title_bar(self):
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #000000;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        title_layout.setSpacing(0)
        
        app_title = QLabel("Deskling")
        app_title.setStyleSheet("color: white; font-size: 13px; font-weight: 600;")
        
        minimize_btn = QPushButton("−")
        minimize_btn.setFixedSize(40, 40)
        minimize_btn.setCursor(Qt.PointingHandCursor)
        minimize_btn.setStyleSheet(self.get_title_button_style())
        minimize_btn.clicked.connect(self.hide_to_tray)
        
        maximize_btn = QPushButton("□")
        maximize_btn.setFixedSize(40, 40)
        maximize_btn.setCursor(Qt.PointingHandCursor)
        maximize_btn.setStyleSheet(self.get_title_button_style())
        maximize_btn.clicked.connect(self.toggle_maximize)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(self.get_title_button_style("#E81123"))
        close_btn.clicked.connect(self.close)  # Use close() to trigger closeEvent, not quit
        
        title_layout.addWidget(app_title)
        title_layout.addStretch()
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)
        
        return title_bar
    
    def get_title_button_style(self, hover_color="#282828"):
        return f"""
            QPushButton {{
                background-color: transparent;
                color: #CCCCCC;
                border: none;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                color: white;
            }}
        """
    
    def change_page(self, page_id):
        page_map = {
            "dashboard": 0,
            "tasks": 1,
            "focus": 2,
            "checkin": 3,
            "settings": 4
        }
        
        if page_id in page_map:
            self.pages.setCurrentIndex(page_map[page_id])
            self.sidebar.change_page(page_id)
    
    def toggle_maximize(self):
        if self.is_maximized:
            if self.normal_geometry:
                self.setGeometry(self.normal_geometry)
            self.is_maximized = False
        else:
            self.normal_geometry = self.geometry()
            from PyQt5.QtWidgets import QDesktopWidget
            screen = QDesktopWidget().availableGeometry()
            self.setGeometry(screen)
            self.is_maximized = True
    
    def center_window(self):
        from PyQt5.QtWidgets import QDesktopWidget
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def setup_timer(self):
        self.check_in_timer = QTimer()
        self.check_in_timer.timeout.connect(self.perform_check_in)
    
    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.white)
        from PyQt5.QtGui import QPainter, QColor, QFont
        painter = QPainter(pixmap)
        painter.setPen(QColor(0, 0, 0))
        font = QFont("Arial", 32)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "🦊")
        painter.end()
        
        icon = QIcon(pixmap)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("Deskling - AI Assistant")
        
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_from_tray)
        
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(logout_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # Make sure tray icon is visible
        self.tray_icon.setVisible(True)
        self.tray_icon.show()
        print("System tray icon shown")
    
    def hide_to_tray(self):
        self.hide()
    
    def show_from_tray(self):
        print("Showing from tray")
        self.show()
        self.raise_()
        self.activateWindow()
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_from_tray()
    
    def perform_check_in(self):
        if self.is_active:
            message = self.assistant.get_ai_check_in(self)
            self.dashboard_page.message_display.setText(message)
            
            if self.db.is_connected() and self.user_id:
                self.db.increment_check_ins(self.user_id)
                self.db.update_user_stats(self.user_id)
    
    def logout(self):
        # End active session
        if self.is_active:
            self.toggle_assistant()
        
        self.session_manager.clear_session()
        
        if self.db.is_connected():
            self.db.sign_out()
        
        # Close compact avatar if active
        if hasattr(self, 'compact_avatar') and self.compact_avatar:
            self.compact_avatar.close()
        if hasattr(self, 'chat_bubble') and self.chat_bubble:
            self.chat_bubble.close()
        
        self.tray_icon.hide()
        
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        
        self.is_logging_out = True
        self.close()
    
    def quit_application(self):
        if self.is_active and self.db.is_connected() and self.user_id and self.current_session_id:
            self.db.end_session(self.current_session_id)
            self.db.update_user_stats(self.user_id)
        
        # Close compact avatar if active
        if hasattr(self, 'compact_avatar') and self.compact_avatar:
            self.compact_avatar.close()
        if hasattr(self, 'chat_bubble') and self.chat_bubble:
            self.chat_bubble.close()
        
        self.tray_icon.hide()
        self.is_quitting = True  # Set flag before closing
        
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
    
    def show_chat_bubble(self):
        if hasattr(self, 'compact_avatar') and self.compact_avatar:
            if hasattr(self, 'pet_menu') and self.pet_menu and self.pet_menu.isVisible():
                self.pet_menu.close()
                self.pet_menu = None
                print("Pet menu closed")
                return
            
            tasks = []
            if hasattr(self, 'tasks_page') and self.tasks_page:
                tasks = self.tasks_page.tasks
            
            focus_page = None
            if hasattr(self, 'focus_page'):
                focus_page = self.focus_page
            
            from ui.pet_menu import PetMenu
            self.pet_menu = PetMenu(self.assistant, tasks, focus_page, self)
            self.pet_menu.closed.connect(self.on_pet_menu_closed)
            
            self.pet_menu.show()
            
            avatar_pos = self.compact_avatar.pos()
            self.pet_menu.update_position(avatar_pos)
            print("Pet menu shown")
    
    def update_pet_menu_position(self, new_pos):
        if hasattr(self, 'pet_menu') and self.pet_menu and self.pet_menu.isVisible():
            self.pet_menu.update_position(new_pos)
    
    def on_pet_menu_closed(self):
        print("Pet menu closed")
        if hasattr(self, 'pet_menu'):
            self.pet_menu = None
    
    def toggle_assistant(self):
        self.is_active = not self.is_active
        
        if self.is_active:
            if self.db.is_connected() and self.user_id:
                session_id = self.db.create_session(self.user_id)
                if session_id:
                    self.current_session_id = session_id
                    self.session_start_time = datetime.now()
                self.db.update_user_stats(self.user_id)
            
            self.check_in_timer.start(15 * 60 * 1000)
            
            from ui.compact_avatar import CompactAvatar
            
            self.compact_avatar = CompactAvatar(self.assistant)
            self.compact_avatar.show()
            
            self.compact_avatar.clicked.connect(self.show_chat_bubble)
            self.compact_avatar.moved.connect(self.update_pet_menu_position)
            
            print("Compact avatar shown")
            
            self.dashboard_page.toggle_button.setText("Turn off AI assistant")
            self.dashboard_page.status_label.setText("● Active")
            self.dashboard_page.status_label.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 600;")
        else:
            if hasattr(self, 'pet_menu') and self.pet_menu:
                self.pet_menu.close()
                self.pet_menu = None
            
            if hasattr(self, 'compact_avatar') and self.compact_avatar:
                self.compact_avatar.close()
                self.compact_avatar = None
                print("Compact avatar hidden")
            
            if self.db.is_connected() and self.user_id and self.current_session_id:
                self.db.end_session(self.current_session_id)
                self.db.update_user_stats(self.user_id)
            
            self.check_in_timer.stop()
            
            self.dashboard_page.toggle_button.setText("Turn on AI assistant")
            self.dashboard_page.status_label.setText("● Inactive")
            self.dashboard_page.status_label.setStyleSheet("color: #9CA3AF; margin-top: 8px;")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 40:
            self.dragging = True
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.dragging and self.offset and not self.is_maximized:
            self.move(self.mapToGlobal(event.pos() - self.offset))
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
    
    def closeEvent(self, event):
        print(f"closeEvent called: is_quitting={self.is_quitting}, is_logging_out={self.is_logging_out}")
        
        if self.is_quitting or self.is_logging_out:
            print("App closing (quit or logout)")
            event.accept()
            return
        
        print("Close event triggered - hiding to tray")
        event.ignore()
        self.hide()
        
        # Make sure tray icon is visible
        print(f"Tray icon visible: {self.tray_icon.isVisible()}")
        if not self.tray_icon.isVisible():
            print("Showing tray icon...")
            self.tray_icon.show()
        
        print("App hidden to tray - window should still be running")
