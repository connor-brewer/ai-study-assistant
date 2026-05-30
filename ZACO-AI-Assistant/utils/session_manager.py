"""
Session Manager - Handles persistent user sessions
"""
from PyQt5.QtCore import QSettings
import json

class SessionManager:
    """Manages user session persistence"""
    
    def __init__(self):
        self.settings = QSettings("Deskling", "UserSession")
    
    def save_session(self, user_data, session_data=None):
        """Save user session data"""
        try:
            # Save user data
            self.settings.setValue("user_id", user_data.get("id"))
            self.settings.setValue("username", user_data.get("username"))
            self.settings.setValue("email", user_data.get("email"))
            self.settings.setValue("avatar_url", user_data.get("avatar_url"))
            self.settings.setValue("total_sessions", user_data.get("total_sessions", 0))
            self.settings.setValue("total_check_ins", user_data.get("total_check_ins", 0))
            self.settings.setValue("total_focus_time", user_data.get("total_focus_time", 0))
            
            # Save session tokens if available
            if session_data:
                if hasattr(session_data, 'access_token'):
                    self.settings.setValue("access_token", session_data.access_token)
                    self.settings.setValue("refresh_token", getattr(session_data, 'refresh_token', None))
                elif isinstance(session_data, dict):
                    self.settings.setValue("access_token", session_data.get('access_token'))
                    self.settings.setValue("refresh_token", session_data.get('refresh_token'))
            
            self.settings.setValue("is_logged_in", True)
            self.settings.sync()
            print("Session saved successfully")
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def load_session(self):
        """Load saved session data"""
        try:
            if not self.settings.value("is_logged_in", False, type=bool):
                return None
            
            user_data = {
                "id": self.settings.value("user_id"),
                "username": self.settings.value("username"),
                "email": self.settings.value("email"),
                "avatar_url": self.settings.value("avatar_url"),
                "total_sessions": self.settings.value("total_sessions", 0, type=int),
                "total_check_ins": self.settings.value("total_check_ins", 0, type=int),
                "total_focus_time": self.settings.value("total_focus_time", 0, type=int),
            }
            
            # Load session tokens if available
            access_token = self.settings.value("access_token")
            refresh_token = self.settings.value("refresh_token")
            
            session_data = None
            if access_token:
                session_data = {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            
            print(f"Session loaded for user: {user_data.get('username')}")
            return {
                "user_data": user_data,
                "session_data": session_data
            }
        except Exception as e:
            print(f"Error loading session: {e}")
            return None
    
    def clear_session(self):
        """Clear saved session (logout)"""
        try:
            self.settings.clear()
            self.settings.sync()
            print("Session cleared")
            return True
        except Exception as e:
            print(f"Error clearing session: {e}")
            return False
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.settings.value("is_logged_in", False, type=bool)

# Singleton instance
_session_manager = None

def get_session_manager():
    """Get or create SessionManager singleton"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

