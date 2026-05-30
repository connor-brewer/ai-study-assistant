"""
Registration Window - New user registration
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database.supabase_client import get_supabase_client

class RegisterWindow(QWidget):
    registration_success = pyqtSignal(dict)  # Signal with user data
    
    def __init__(self):
        super().__init__()
        self.db = get_supabase_client()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the registration window UI"""
        self.setWindowTitle("Deskling - Register")
        self.setFixedSize(420, 580)
        
        # Center window on screen
        self.center_window()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(45, 50, 45, 45)
        layout.setSpacing(12)
        
        # Avatar/Icon
        icon_label = QLabel("🦊")
        icon_font = QFont("Arial", 64)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("Create Account")
        title_font = QFont("Segoe UI", 26, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Subtitle
        subtitle_label = QLabel("Join us and stay focused!")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #777777;")
        
        # Spacing
        layout.addSpacing(5)
        layout.addWidget(icon_label)
        layout.addSpacing(5)
        layout.addWidget(title_label)
        layout.addSpacing(5)
        layout.addWidget(subtitle_label)
        layout.addSpacing(30)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #555555; font-size: 12px; font-weight: 600;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setMinimumHeight(44)
        
        # Email field
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #555555; font-size: 12px; font-weight: 600;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(44)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #555555; font-size: 12px; font-weight: 600;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(44)
        
        # Confirm Password field
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("color: #555555; font-size: 12px; font-weight: 600;")
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setMinimumHeight(44)
        self.confirm_input.returnPressed.connect(self.handle_register)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.setMinimumHeight(48)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.handle_register)
        
        # Back to login link
        back_layout = QHBoxLayout()
        back_text = QLabel("Already have an account?")
        back_text.setStyleSheet("color: #777777; font-size: 12px;")
        self.back_link = QPushButton("Login")
        self.back_link.setFlat(True)
        self.back_link.setCursor(Qt.PointingHandCursor)
        self.back_link.setStyleSheet("""
            QPushButton {
                color: #2C2C2C;
                font-size: 12px;
                font-weight: 600;
                text-decoration: underline;
                border: none;
                background: transparent;
                padding: 0px;
            }
            QPushButton:hover {
                color: #1A1A1A;
            }
        """)
        self.back_link.clicked.connect(self.close)
        back_layout.addStretch()
        back_layout.addWidget(back_text)
        back_layout.addWidget(self.back_link)
        back_layout.addStretch()
        
        # Add widgets to layout
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addSpacing(10)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addSpacing(10)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addSpacing(20)
        layout.addWidget(self.register_button)
        layout.addSpacing(12)
        layout.addLayout(back_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Apply modern, aesthetic styling
        self.setStyleSheet("""
            QWidget {
                background-color: #FAFAFA;
                color: #2C2C2C;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #2C2C2C;
            }
            QLineEdit:focus {
                border: 2px solid #4A4A4A;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #AAAAAA;
            }
            QPushButton {
                background-color: #2C2C2C;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
            }
            QPushButton:pressed {
                background-color: #1A1A1A;
            }
        """)
    
    def center_window(self):
        """Center the window on the screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def handle_register(self):
        """Handle registration"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validation
        if not username or not email or not password:
            QMessageBox.warning(self, "Registration Failed",
                              "Please fill in all fields.")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "Registration Failed",
                              "Username must be at least 3 characters long.")
            return
        
        if '@' not in email:
            QMessageBox.warning(self, "Registration Failed",
                              "Please enter a valid email address.")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Registration Failed",
                              "Password must be at least 6 characters long.")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Registration Failed",
                              "Passwords do not match.")
            return
        
        # Check if database is configured
        if not self.db.is_connected():
            QMessageBox.information(self, "Offline Mode",
                                  "Database not configured. Account created in demo mode.")
            user_data = {"username": username, "email": email, "id": "demo"}
            self.registration_success.emit(user_data)
            return
        
        # Create user with Supabase Auth
        result = self.db.sign_up_with_email(email, password, username)
        
        if result["success"]:
            # Get the created user profile
            user_profile = self.db.get_user_by_email(email)
            if user_profile:
                self.registration_success.emit(user_profile)
            else:
                # Fallback data
                self.registration_success.emit({
                    "username": username,
                    "email": email,
                    "id": result["user"].id
                })
        else:
            error_msg = result.get('error', 'Unknown error')
            # Better error messages
            if 'already registered' in error_msg.lower() or 'already exists' in error_msg.lower():
                QMessageBox.warning(self, "Registration Failed",
                                  "An account with this email already exists.\n\n"
                                  "Please use the login page instead.")
            else:
                QMessageBox.critical(self, "Registration Failed",
                                   f"Error creating account: {error_msg}")

