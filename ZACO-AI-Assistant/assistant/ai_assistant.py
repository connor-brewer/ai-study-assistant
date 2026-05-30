import os
import random
import secrets
import base64
from datetime import datetime
import google.generativeai as genai
from PyQt5.QtWidgets import QMessageBox

class AIAssistant:
    def __init__(self, username):


        self.username = username
        self.check_in_count = 0
        




        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        


        



        self.chat_history = []
        
        self.check_in_messages = [
            f"Hey {username}, how's the task going? Still focused?",
            f"{username}, just checking in! Are you making progress?",
            f"Quick check-in, {username}! Are you staying on track?",
            f"Hi {username}! How are you doing with your current task?",
            f"{username}, time for a focus check! Still working hard?",
            f"Hey there {username}! Let me know you're still on it!",
            f"{username}, don't get distracted! How's it going?",
            f"Checking in, {username}! Are you staying productive?",
            f"{username}, quick question: are you still focused on your goal?",
            f"Hey {username}, just making sure you're staying accountable!",
        ]
        
        self.motivational_messages = [
            "You're doing great! Keep up the momentum!",
            "Remember why you started. You've got this!",
            "Every minute of focus counts. Stay strong!",
            "I believe in you! Keep pushing forward!",
            "Focus now, celebrate later. You're on the right path!",
        ]
    















    def get_check_in_message(self):
        self.check_in_count += 1
        
        if self.check_in_count % 3 == 0:
            motivation = random.choice(self.motivational_messages)
            return f"{random.choice(self.check_in_messages)} {motivation}"
        
        return random.choice(self.check_in_messages)
    

    
    def get_time_based_greeting(self):
        hour = datetime.now().hour
        
        if hour < 12:
            return f"Good morning, {self.username}!"
        elif hour < 18:
            return f"Good afternoon, {self.username}!"
        else:
            return f"Good evening, {self.username}!"
    


    def get_interaction_message(self):
        interaction_messages = [
            f"Hey {self.username}! Just checking - you still focused?",
            f"Hi there! Need any help staying on track?",
            f"You called? Everything going well?",
            f"What's up, {self.username}? Still working hard?",
            f"Hey! Just your friendly reminder to stay focused! 😊",
            f"Looking good, {self.username}! Keep up the great work!",
            f"Need a pep talk? You've got this!",
            f"Checking in! How's the progress coming along?",
            f"Hi {self.username}! Remember why you started!",
            f"You're doing amazing! Keep going!",
            f"Hey there! Time to buckle down and focus!",
            f"What's the status, {self.username}? On task?",
            f"Just here to remind you - you're capable of great things!",
            f"Taking a break or staying focused? Either is fine!",
            f"Hey {self.username}! Let's get back to it!",
        ]
        
        return random.choice(interaction_messages)
    




    def send_message_with_alert(self, user_message, parent_widget=None):
        try:
            context = f"You are a friendly productivity assistant helping {self.username} stay focused and motivated. Keep responses brief and encouraging."
            

            prompt = f"{context}\n\nUser: {user_message}\n\nAssistant:"
            if self.model is not None:
                response = self.model.generate_content(prompt)
                ai_response = response.text
            else:
                # Fallback: generate a short canned response when AI is unavailable
                ai_response = self.get_interaction_message()
            
            self.chat_history.append({
                "user": user_message,
                "assistant": ai_response,
                "timestamp": datetime.now()
            })
            
            

            self.show_alert("AI Assistant Response", ai_response, parent_widget)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Error communicating with AI: {str(e)}"
            print(error_msg)
            self.show_alert("Error", error_msg, parent_widget)
            return None
    




    def show_alert(self, title, message, parent_widget=None):
        msg_box = QMessageBox(parent_widget)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    




    def get_ai_check_in(self, parent_widget=None):
        try:
            prompt = f"Generate a brief, friendly check-in message for {self.username} to help them stay focused on their tasks. Keep it under 30 words and encouraging."
            if self.model is not None:
                response = self.model.generate_content(prompt)
                ai_message = response.text
                self.show_alert("Focus Check-In", ai_message, parent_widget)
                return ai_message
            else:
                # Fallback to offline check-in
                fallback_msg = self.get_check_in_message()
                self.show_alert("Focus Check-In", fallback_msg, parent_widget)
                return fallback_msg
            
        except Exception as e:
            print(f"AI check-in failed: {e}")
            fallback_msg = self.get_check_in_message()
            self.show_alert("Focus Check-In", fallback_msg, parent_widget)
            return fallback_msg

