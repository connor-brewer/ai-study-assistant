from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QSpinBox, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
import math
import random


class CheckinPage(QWidget):

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.username = user_data.get('username', 'User') if isinstance(user_data, dict) else str(user_data)
        self.timer_active = False
        self.punishment = self.user_data.get("punishment", False)


        self.checkin_frequency = self.user_data.get("checkin_frequency", "Low")

        self.time_remaining = 0
        self.checkin_intervals = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.init_ui()





    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(20)

        header = QLabel("Check-In Timer")
        header_font = QFont("Segoe UI", 26, QFont.Bold)
        header.setFont(header_font)
        header.setStyleSheet("color: #111827;")
        header.setAlignment(Qt.AlignLeft)

        subtitle_label = QLabel("A timer, but Zaco periodically checks in on you.")
        subtitle_font = QFont("Segoe UI", 13)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6B7280;")
        subtitle_label.setWordWrap(True)

        
        




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



        custom_timer_label = QLabel("Set Custom Timer (minutes) and (seconds):")
        custom_timer_label.setFont(QFont("Segoe UI", 13))
        


        self.custom_timer_input_minute = QSpinBox()
        self.custom_timer_input_minute.setRange(0, 300) 
        self.custom_timer_input_minute.setValue(0)  
        self.custom_timer_input_minute.setFixedWidth(100)
        self.custom_timer_input_minute.setStyleSheet("font-size: 20px; color: #6366F1;")

        self.custom_timer_input_second = QSpinBox()
        self.custom_timer_input_second.setRange(0, 59) 
        self.custom_timer_input_second.setValue(0)  
        self.custom_timer_input_second.setFixedWidth(100)
        self.custom_timer_input_second.setStyleSheet("font-size: 20px; color: #6366F1;")




        self.set_custom_timer_btn = QPushButton("Set Custom Timer")
        self.set_custom_timer_btn.clicked.connect(self.set_custom_timer)
        


        self.punishment_checkbox = QCheckBox("Enable punishment mode?")
        self.punishment_checkbox.setChecked(self.punishment)
        self.punishment_checkbox.stateChanged.connect(self.toggle_punishment)



        self.checkin_frequency_dropdown = QComboBox()
        self.checkin_frequency_dropdown.addItem('Low')
        self.checkin_frequency_dropdown.addItem('Medium')
        self.checkin_frequency_dropdown.addItem('High')
        index = self.checkin_frequency_dropdown.findText(self.checkin_frequency)
        self.checkin_frequency_dropdown.setCurrentIndex(index if index >= 0 else 0)
        self.checkin_frequency_dropdown.currentTextChanged.connect(self.toggle_checkin_frequency)



        
        layout.addWidget(header)
        layout.addWidget(subtitle_label)
        layout.addSpacing(10)
        layout.addWidget(custom_timer_label, alignment=Qt.AlignHCenter)
        layout.addSpacing(10)

        an_input_row = QHBoxLayout()
        an_input_row.addStretch(1)
        an_input_row.addWidget(self.punishment_checkbox, alignment=Qt.AlignLeft)
        an_input_row.addSpacing(200)
        frequency_label = QLabel("Check-In frequency?")
        an_input_row.addWidget(frequency_label)
        an_input_row.addSpacing(2)
        an_input_row.addWidget(self.checkin_frequency_dropdown, alignment=Qt.AlignRight)
        an_input_row.addStretch(1)
        layout.addLayout(an_input_row)

        timer_input_row = QHBoxLayout()
        timer_input_row.addStretch(1)
        timer_input_row.addWidget(self.custom_timer_input_minute)
        timer_input_row.addSpacing(10)
        timer_input_row.addWidget(self.custom_timer_input_second)
        timer_input_row.addSpacing(10)
        timer_input_row.addWidget(self.set_custom_timer_btn)
        timer_input_row.addStretch(1)
        layout.addLayout(timer_input_row)

        layout.addSpacing(10)
        layout.addWidget(self.timer_display)

        layout.addSpacing(10)
        layout.addLayout(controls_layout)




        layout.addStretch()
        self.setLayout(layout)





    def toggle_punishment(self, state):
        self.punishment = bool(state)
        self.user_data["punishment"] = self.punishment
        print(f"Punishment toggled to: {bool(state)}")



    def toggle_checkin_frequency(self, text):
        self.checkin_frequency = text
        self.user_data["checkin_frequency"] = text
        print(f"Check-In frequency set to: {text}")





    def generate_random_intervals(self, minutes_time, frequency):  #time in minutes     frequency = []"Low", "Medium", "High"]
        timesarr = []
        # flat first 5 minutes, never can recieve a prompt

        if minutes_time <= 5:
            return []

        # pick intervals, choose a random time in the later half of that interval
        base_interval = 0.0


        if (frequency == "Low"):                   # every 40 minutes
            base_interval = 40

        elif (frequency == "Medium"):              # every 30 minutes
            base_interval = 30
        else:                                      # every 20 minutes 
            base_interval = 20



        num_intervals = math.floor((minutes_time)/base_interval)
        for i in range(num_intervals):
            val = base_interval*(i+1)
            randval = random.randint(int(val - (base_interval/2)), int(val))
            timesarr.append(randval)



        for i in range(len(timesarr)):
            timesarr[i] = timesarr[i] + 5

        if timesarr:  #its not empty
            timesarr = [x for x in timesarr if x < minutes_time]

        return timesarr













    def set_custom_timer(self):
        minutes = self.custom_timer_input_minute.value()
        seconds = self.custom_timer_input_second.value()
        self.time_remaining = minutes * 60 + seconds
        self.update_display()
        self.start_btn.setEnabled(self.time_remaining > 0)
        print(f"Custom timer set: {minutes} minutes and {seconds} seconds")




    
    def select_duration(self, minutes):
        self.time_remaining = minutes * 60  # Convert to seconds
        self.update_display()
        self.start_btn.setEnabled(True)
        print(f"Selected {minutes} minutes focus session")
    


    def start_timer(self):
        if self.time_remaining > 0:
            darr = self.generate_random_intervals(self.time_remaining/60 , self.checkin_frequency)
            print("The generated check-in intervals are: ", darr)
            self.checkin_intervals = darr
            self.timer_active = True
            self.timer.start(1000)  # Update every second
            self.start_btn.setVisible(False)
            self.stop_btn.setVisible(True)
            print(f"Focus timer started: {self.time_remaining} seconds")
    


    def stop_timer(self):
        self.timer_active = False
        self.timer.stop()
        self.time_remaining = 0
        self.checkin_intervals = []
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













