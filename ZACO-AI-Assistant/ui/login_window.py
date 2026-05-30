"""
Login Window - Authentication interface for the AI Companion
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from ui.overlay_window import OverlayWindow
from database.supabase_client import get_supabase_client
from utils.session_manager import get_session_manager
import webbrowser

class OAuthSignals(QObject):
    """Signals for OAuth callback handling"""
    code_received = pyqtSignal(str)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.overlay_window = None
        self.db = get_supabase_client()
        self.session_manager = get_session_manager()
        self.oauth_signals = OAuthSignals()
        self.oauth_signals.code_received.connect(self.process_oauth_code)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the login window UI"""
        self.setWindowTitle("Deskling - Login")
        self.setFixedSize(1000, 650)
        
        # Remove default window frame for custom controls
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Center window on screen
        self.center_window()
        
        # For dragging window
        self.dragging = False
        self.offset = None
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #1A1A1A;")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(15, 0, 10, 0)
        
        app_title = QLabel("Deskling")
        app_title.setStyleSheet("color: white; font-size: 13px; font-weight: 600;")
        
        # Window control buttons
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #CCCCCC;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #E81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        title_bar_layout.addWidget(app_title)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_btn)
        
        # Content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left side - Branding with gradient
        left_side = QWidget()
        left_side.setFixedWidth(480)
        left_side.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #6366F1, stop:1 #8B5CF6);
        """)
        left_layout = QVBoxLayout(left_side)
        left_layout.setContentsMargins(60, 100, 60, 100)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Icon with background circle
        icon_container = QWidget()
        icon_container.setFixedSize(140, 140)
        icon_container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 70px;
            border: 3px solid rgba(255, 255, 255, 0.3);
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        brand_icon = QLabel("🦊")
        brand_icon.setAlignment(Qt.AlignCenter)
        brand_icon_font = QFont("Arial", 72)
        brand_icon.setFont(brand_icon_font)
        icon_layout.addWidget(brand_icon)
        
        icon_center_layout = QHBoxLayout()
        icon_center_layout.addStretch()
        icon_center_layout.addWidget(icon_container)
        icon_center_layout.addStretch()
        
        brand_title = QLabel("Deskling")
        brand_title.setAlignment(Qt.AlignCenter)
        brand_title_font = QFont("Segoe UI", 38, QFont.Bold)
        brand_title.setFont(brand_title_font)
        brand_title.setStyleSheet("color: white; margin-top: 30px;")
        
        brand_subtitle = QLabel("Your intelligent focus partner")
        brand_subtitle.setAlignment(Qt.AlignCenter)
        brand_subtitle_font = QFont("Segoe UI", 15)
        brand_subtitle.setFont(brand_subtitle_font)
        brand_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); margin-top: 12px;")
        
        features_label = QLabel("✓ Smart Check-ins\n✓ Task Management\n✓ Focus Tracking")
        features_label.setAlignment(Qt.AlignCenter)
        features_font = QFont("Segoe UI", 13)
        features_label.setFont(features_font)
        features_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            margin-top: 40px;
            line-height: 28px;
        """)
        
        left_layout.addLayout(icon_center_layout)
        left_layout.addWidget(brand_title)
        left_layout.addWidget(brand_subtitle)
        left_layout.addWidget(features_label)
        left_layout.addStretch()
        
        # Right side - Login form
        right_side = QWidget()
        right_side.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(right_side)
        layout.setContentsMargins(80, 0, 80, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)
        
        # Welcome text
        welcome_label = QLabel("Welcome Back")
        welcome_font = QFont("Segoe UI", 36, QFont.Bold)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #1A1A1A;")
        
        # Subtitle
        subtitle_label = QLabel("Sign in to continue your journey")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666; margin-top: 12px;")
        
        # Spacing
        spacer1 = QWidget()
        spacer1.setFixedHeight(60)
        
        # Google login button with icon
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(12)
        
        self.google_button = QPushButton("🌐  Continue with Google")
        self.google_button.setMinimumHeight(56)
        self.google_button.setFixedWidth(340)
        self.google_button.setCursor(Qt.PointingHandCursor)
        self.google_button.setObjectName("googleButton")
        self.google_button.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 0.5px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
        """)
        self.google_button.clicked.connect(self.handle_google_login)
        
        helper_text = QLabel("Secure authentication via Google OAuth")
        helper_text.setAlignment(Qt.AlignCenter)
        helper_font = QFont("Segoe UI", 11)
        helper_text.setFont(helper_font)
        helper_text.setStyleSheet("color: #999999;")
        
        button_layout.addWidget(self.google_button)
        button_layout.addWidget(helper_text)
        
        # Add widgets to layout
        layout.addWidget(welcome_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(spacer1)
        layout.addWidget(button_container)
        
        # Assemble content
        content_layout.addWidget(left_side)
        content_layout.addWidget(right_side)
        
        # Add to main layout
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)
        
        self.setLayout(main_layout)
        
        # Apply modern, aesthetic styling
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    def center_window(self):
        """Center the window on the screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def handle_google_login(self):
        """Handle Google OAuth login via Supabase"""
        if not self.db.is_connected():
            QMessageBox.information(self, "Google Login",
                                  "Database not configured.\n\n"
                                  "Please set up Supabase to use Google login.\n"
                                  "See SUPABASE_AUTH_SETUP.md for details.")
            return
        
        # Import callback handler
        from auth.oauth_callback_handler import start_callback_server
        import threading
        
        # Start local callback server in background
        def wait_for_callback():
            print("Waiting for OAuth callback...")
            callback_data = start_callback_server(port=8080, timeout=120)
            
            print(f"Callback received: {callback_data}")
            
            if callback_data.get('code'):
                code = callback_data.get('code')
                print(f"Emitting code signal: {code}")
                # Emit signal to process in main thread
                self.oauth_signals.code_received.emit(code)
            else:
                print("No callback data received")
        
        server_thread = threading.Thread(target=wait_for_callback)
        server_thread.daemon = True
        server_thread.start()
        
        # Get OAuth URL and open browser
        result = self.db.sign_in_with_google()
        
        if result["success"]:
            webbrowser.open(result["url"])
            # Silently wait for authentication - no popup needed
        else:
            QMessageBox.warning(self, "Error", 
                              f"Failed to initiate Google login: {result.get('error', 'Unknown error')}\n\n"
                              "Make sure Google OAuth is enabled in your Supabase dashboard.")
    
    def process_oauth_code(self, code):
        """Process OAuth code and complete login"""
        print(f"Processing OAuth code: {code}")
        
        if not code:
            QMessageBox.warning(self, "Login Error",
                              "No authorization code received from Google.")
            return
        
        try:
            # Exchange code for session
            print("Exchanging code for session...")
            result = self.db.exchange_code_for_session(code)
            
            print(f"Exchange result: {result.get('success')}")
            
            if result["success"]:
                user_profile = result.get("profile")
                user = result.get("user")
                session_data = result.get("session")
                
                # Extract avatar URL from user metadata
                avatar_url = None
                if user and hasattr(user, 'user_metadata'):
                    avatar_url = user.user_metadata.get('avatar_url') or user.user_metadata.get('picture')
                
                if user_profile:
                    print(f"User profile found: {user_profile.get('username')}")
                    # Add avatar URL to profile
                    user_profile['avatar_url'] = avatar_url
                    # Auto-login without popup and save session
                    self.show_overlay(user_profile, session_data)
                else:
                    print("Creating fallback user data")
                    # Fallback with user data from OAuth
                    user_email = user.email if user and hasattr(user, 'email') else "google@user.com"
                    username = user_email.split('@')[0]
                    
                    user_data = {
                        "username": username,
                        "email": user_email,
                        "id": user.id if user and hasattr(user, 'id') else "google_user",
                        "avatar_url": avatar_url,
                        "total_sessions": 0,
                        "total_check_ins": 0,
                        "total_focus_time": 0
                    }
                    
                    print(f"Logging in as: {username}")
                    print(f"Avatar URL: {avatar_url}")
                    # Auto-login without popup and save session
                    self.show_overlay(user_data, result.get("session"))
            else:
                error = result.get('error', 'Unknown error')
                print(f"Exchange failed: {error}")
                QMessageBox.warning(self, "Login Error",
                                  f"Failed to complete Google login:\n{error}")
            
        except Exception as e:
            print(f"Exception during OAuth processing: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Login Error",
                              f"Error completing Google authentication:\n{str(e)}")
    
    def handle_google_callback_success(self, callback_data):
        """Handle successful Google OAuth callback"""
        code = callback_data.get('code')
        self.process_oauth_code(code)
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.LeftButton and event.y() < 40:
            self.dragging = True
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.dragging and self.offset:
            self.move(self.mapToGlobal(event.pos() - self.offset))
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
    
    def show_overlay(self, user_data, session_data=None):
        """Show the overlay window and hide login"""
        # Save session for persistence
        self.session_manager.save_session(user_data, session_data)
        
        self.overlay_window = OverlayWindow(user_data)
        self.overlay_window.show()
        self.hide()

