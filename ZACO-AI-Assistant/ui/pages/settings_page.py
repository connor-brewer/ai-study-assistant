"""
Settings Page - User settings for Deskling
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SettingsPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.user_id = user_data.get('id')
        self.username = user_data.get('username', 'User')
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Initialize the settings UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 40)
        layout.setSpacing(22)
        
        # Header
        header_label = QLabel("Settings")
        header_font = QFont("Segoe UI", 26, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #111827;")
        
        subtitle_label = QLabel("Manage your account and preferences")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6B7280;")
        
        # Profile section title
        profile_title = QLabel("Profile")
        profile_title_font = QFont("Segoe UI", 18, QFont.Bold)
        profile_title.setFont(profile_title_font)
        profile_title.setStyleSheet("color: #111827; margin-top: 8px;")
        
        # Profile content card
        profile_card = QFrame()
        profile_card.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        profile_card_layout = QVBoxLayout(profile_card)
        profile_card_layout.setContentsMargins(0, 0, 0, 0)
        profile_card_layout.setSpacing(16)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #6B7280; font-size: 13px; font-weight: 500;")
        
        self.username_input = QLineEdit()
        self.username_input.setText(self.username)
        self.username_input.setMinimumHeight(42)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 11px 14px;
                font-size: 14px;
                color: #1F2937;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
                background-color: white;
            }
        """)
        
        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.setMinimumHeight(46)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #4338CA;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        
        profile_card_layout.addWidget(username_label)
        profile_card_layout.addWidget(self.username_input)
        profile_card_layout.addSpacing(8)
        profile_card_layout.addWidget(save_btn)
        
        # Account section title
        account_title = QLabel("Account")
        account_title_font = QFont("Segoe UI", 18, QFont.Bold)
        account_title.setFont(account_title_font)
        account_title.setStyleSheet("color: #111827; margin-top: 8px;")
        
        # Account content card
        account_card = QFrame()
        account_card.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        account_card_layout = QVBoxLayout(account_card)
        account_card_layout.setContentsMargins(0, 0, 0, 0)
        account_card_layout.setSpacing(14)
        
        logout_desc = QLabel("Sign out of your account")
        logout_desc.setStyleSheet("color: #6B7280; font-size: 13px;")
        logout_desc.setWordWrap(True)
        
        logout_btn = QPushButton("Sign Out")
        logout_btn.setMinimumHeight(46)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #DC2626;
                border: 1px solid #FCA5A5;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #FEF2F2;
                border: 1px solid #F87171;
            }
            QPushButton:pressed {
                background-color: #FEE2E2;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        
        account_card_layout.addWidget(logout_desc)
        account_card_layout.addWidget(logout_btn)
        
        # Add widgets
        layout.addWidget(header_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(32)
        layout.addWidget(profile_title)
        layout.addSpacing(12)
        layout.addWidget(profile_card)
        layout.addSpacing(28)
        layout.addWidget(account_title)
        layout.addSpacing(12)
        layout.addWidget(account_card)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def save_settings(self):
        """Save user settings"""
        new_username = self.username_input.text().strip()
        if not new_username:
            return
        
        if self.db.is_connected() and self.user_id:
            try:
                self.db.client.table('users').update({
                    'username': new_username
                }).eq('id', self.user_id).execute()
                
                self.username = new_username
                self.user_data['username'] = new_username
                print(f"Username updated to: {new_username}")
            except Exception as e:
                print(f"Error updating settings: {e}")
    
    def logout(self):
        """Handle logout"""
        # Get parent OverlayWindow and call its logout method
        from PyQt5.QtWidgets import QApplication
        for widget in QApplication.topLevelWidgets():
            if widget.__class__.__name__ == 'OverlayWindow':
                widget.logout()
                break

