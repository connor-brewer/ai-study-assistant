from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta

class FocusPage(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.timer_active = False
        self.time_remaining = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(24)
        
        header_label = QLabel("⏱️ Focus Timer")
        header_font = QFont("Segoe UI", 26, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #111827;")
        
        subtitle_label = QLabel("Select a focus duration and stay productive!")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6B7280;")
        
        self.timer_display = QLabel("00:00")
        timer_font = QFont("Segoe UI", 72, QFont.Bold)
        self.timer_display.setFont(timer_font)
        self.timer_display.setAlignment(Qt.AlignCenter)
        self.timer_display.setStyleSheet("""
            color: #6366F1;
            background-color: white;
            border-radius: 20px;
            padding: 40px;
            margin: 20px 0;
        """)
        
        durations_label = QLabel("Quick Select")
        durations_font = QFont("Segoe UI", 16, QFont.Bold)
        durations_label.setFont(durations_font)
        durations_label.setStyleSheet("color: #111827;")
        
        durations_container = QWidget()
        durations_layout = QGridLayout(durations_container)
        durations_layout.setSpacing(16)
        
        presets = [
            (5, "5 min", "Quick Break"),
            (15, "15 min", "Short Focus"),
            (25, "25 min", "Pomodoro"),
            (45, "45 min", "Deep Work"),
            (60, "60 min", "Hour Session"),
            (90, "90 min", "Extended")
        ]
        
        for idx, (minutes, title, subtitle) in enumerate(presets):
            btn = self.create_duration_button(minutes, title, subtitle)
            row = idx // 3
            col = idx % 3
            durations_layout.addWidget(btn, row, col)
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(16)
        
        self.start_btn = QPushButton("Start Focus Session")
        self.start_btn.setFixedHeight(56)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
            QPushButton:disabled {
                background-color: #9CA3AF;
            }
        """)
        self.start_btn.clicked.connect(self.start_timer)
        self.start_btn.setEnabled(False)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedHeight(56)
        self.stop_btn.setFixedWidth(120)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.stop_btn.setVisible(False)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.stop_btn)
        
        layout.addWidget(header_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(self.timer_display)
        layout.addSpacing(16)
        layout.addWidget(durations_label)
        layout.addWidget(durations_container)
        layout.addSpacing(24)
        layout.addLayout(controls_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_duration_button(self, minutes, title, subtitle):
        btn = QPushButton()
        btn.setFixedHeight(100)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty("minutes", minutes)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 14px;
                text-align: center;
            }
            QPushButton:hover {
                border: 2px solid #6366F1;
                background-color: #EEF2FF;
            }
        """)
        
        btn_layout = QVBoxLayout(btn)
        btn_layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #111827;")
        
        subtitle_label = QLabel(subtitle)
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #6B7280;")
        
        btn_layout.addWidget(title_label)
        btn_layout.addWidget(subtitle_label)
        
        btn.clicked.connect(lambda: self.select_duration(minutes))
        
        return btn
    
    def select_duration(self, minutes):
        self.time_remaining = minutes * 60  # Convert to seconds
        self.update_display()
        self.start_btn.setEnabled(True)
        print(f"Selected {minutes} minutes focus session")
    
    def start_timer(self):
        if self.time_remaining > 0:
            self.timer_active = True
            self.timer.start(1000)  # Update every second
            self.start_btn.setVisible(False)
            self.stop_btn.setVisible(True)
            print(f"Focus timer started: {self.time_remaining} seconds")
    
    def stop_timer(self):
        self.timer_active = False
        self.timer.stop()
        self.time_remaining = 0
        self.update_display()
        self.start_btn.setVisible(True)
        self.start_btn.setEnabled(False)
        self.stop_btn.setVisible(False)
        print("Focus timer stopped")
    
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.timer_active = False
            self.notify_timer_complete()
    
    def update_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_display.setText(f"{minutes:02d}:{seconds:02d}")
    
    def notify_timer_complete(self):
        self.timer_display.setStyleSheet("""
            color: #10B981;
            background-color: white;
            border-radius: 20px;
            padding: 40px;
            margin: 20px 0;
        """)
        self.timer_display.setText("✓ Done!")
        
        from PyQt5.QtWidgets import QSystemTrayIcon
        from PyQt5.QtWidgets import QApplication
        
        print("🎉 Focus session complete!")
        
        QTimer.singleShot(3000, self.reset_display)
    
    def reset_display(self):
        self.timer_display.setStyleSheet("""
            color: #6366F1;
            background-color: white;
            border-radius: 20px;
            padding: 40px;
            margin: 20px 0;
        """)
        self.timer_display.setText("00:00")
        self.start_btn.setVisible(True)
        self.start_btn.setEnabled(False)
        self.stop_btn.setVisible(False)
    
    def get_time_remaining_str(self):
        if self.timer_active and self.time_remaining > 0:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            return f"{minutes:02d}:{seconds:02d}"
        return None
