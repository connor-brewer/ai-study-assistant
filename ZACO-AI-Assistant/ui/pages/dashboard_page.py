"""
Dashboard Page - Main overview for the AI Companion
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DashboardPage(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.username = user_data.get('username', 'User')
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dashboard UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(20)
        
        # Header
        header_label = QLabel(f"Welcome back, {self.username}! 👋")
        header_font = QFont("Segoe UI", 26, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #111827;")
        
        subtitle_label = QLabel("Here's your productivity overview")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6B7280;")
        
        # Stats cards
        stats_container = QWidget()
        stats_layout = QGridLayout(stats_container)
        stats_layout.setSpacing(20)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        # Get user stats
        total_sessions = self.user_data.get('total_sessions', 0)
        level = self.user_data.get('level', 1)
        xp = self.user_data.get('xp', 0)
        
        stats_data = [
            ("Level", str(level), "⭐"),
            ("XP", str(xp), "✨"),
            ("Sessions", str(total_sessions), "📊")
        ]
        
        for i, (label, value, icon) in enumerate(stats_data):
            card = self.create_stat_card(icon, label, value)
            stats_layout.addWidget(card, 0, i)
        
        # Assistant message area
        message_label = QLabel("Assistant Messages")
        message_font = QFont("Segoe UI", 16, QFont.Bold)
        message_label.setFont(message_font)
        message_label.setStyleSheet("color: #111827;")
        
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setMinimumHeight(100)
        self.message_display.setMaximumHeight(100)
        self.message_display.setText("🦊 Welcome! I'm your AI assistant. Turn me on to stay productive and earn XP!")
        self.message_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                border-radius: 14px;
                padding: 20px 24px;
                font-size: 14px;
                color: #374151;
                line-height: 1.6;
            }
        """)
        
        # Toggle button
        self.toggle_button = QPushButton("Turn on AI assistant")
        self.toggle_button.setMinimumHeight(52)
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 26px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
            QPushButton:pressed {
                background-color: #4338CA;
            }
        """)
        
        # Status
        self.status_label = QLabel("● Inactive")
        status_font = QFont("Segoe UI", 12)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #9CA3AF; margin-top: 8px;")
        
        # Add widgets
        layout.addWidget(header_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(24)
        layout.addWidget(stats_container)
        layout.addSpacing(28)
        layout.addWidget(message_label)
        layout.addSpacing(8)
        layout.addWidget(self.message_display)
        layout.addSpacing(24)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_stat_card(self, icon, label, value):
        """Create a stat card widget"""
        card = QFrame()
        card.setFixedHeight(200)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 16px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 28, 20, 28)
        card_layout.setSpacing(6)
        card_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_font = QFont("Arial", 26)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_font = QFont("Segoe UI", 34, QFont.Bold)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: #111827;")
        
        desc_label = QLabel(label)
        desc_font = QFont("Segoe UI", 13)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #6B7280; font-weight: 500;")
        
        card_layout.addWidget(icon_label)
        card_layout.addWidget(value_label)
        card_layout.addWidget(desc_label)
        
        return card

