"""
Deskling - Student Accountability Assistant
Main entry point for the application
"""
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from ui.login_window import LoginWindow
from ui.overlay_window import OverlayWindow
from utils.session_manager import get_session_manager
from database.supabase_client import get_supabase_client

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Deskling")
    app.setOrganizationName("Deskling")
    
    # Check for existing session
    session_manager = get_session_manager()
    saved_session = session_manager.load_session()
    
    try:
        if saved_session and saved_session.get("user_data"):
            print("Found saved session, auto-logging in...")
            user_data = saved_session["user_data"]
            session_data = saved_session.get("session_data")
            
            # Restore Supabase auth session if we have both tokens
            db = get_supabase_client()
            if db.is_connected() and session_data and session_data.get("access_token") and session_data.get("refresh_token"):
                try:
                    print("Restoring Supabase auth session...")
                    # Set the session in Supabase client
                    db.client.auth.set_session(
                        session_data.get("access_token"),
                        session_data.get("refresh_token")
                    )
                    print("Supabase auth session restored!")
                except Exception as e:
                    print(f"Could not restore auth session: {e}")
                    print("Please log out and log back in to get a fresh session.")
            elif session_data and not session_data.get("refresh_token"):
                print("⚠️ Old session detected without refresh_token.")
                print("⚠️ Please LOGOUT and LOGIN again to see your tasks!")
            
            # Refresh user data from database
            if db.is_connected():
                refreshed_user = db.get_user_by_email(user_data.get("email"))
                if refreshed_user:
                    # Update with latest data
                    user_data.update(refreshed_user)
                    print(f"Session valid, logging in as {user_data.get('username')}")
            
            # Show main window directly
            print("Creating main window...")
            main_window = OverlayWindow(user_data)
            print("Showing main window...")
            main_window.show()
            print("Main window should be visible now")
        else:
            print("No saved session, showing login window...")
            # Show login window
            login_window = LoginWindow()
            login_window.show()
        
        print("Entering event loop...")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

