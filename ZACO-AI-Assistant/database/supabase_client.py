"""
Supabase Database Client - Handles all database operations
"""
import os
from datetime import datetime
from supabase import create_client, Client

# ============================================
# CONFIGURE YOUR SUPABASE CREDENTIALS HERE
# ============================================
# Option 1: Hardcode your credentials (for .exe distribution)
SUPABASE_URL = "your_supabase_url_here"  # e.g., "https://xxxxx.supabase.co"
SUPABASE_KEY = "your_supabase_anon_key_here"  # Your anon/public key

# Option 2: Use environment variables (for development)
# Leave the above as empty strings and create a .env file
# ============================================

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client"""
        # Try hardcoded credentials first, then fall back to .env
        url = SUPABASE_URL if SUPABASE_URL and SUPABASE_URL != "your_supabase_url_here" else None
        key = SUPABASE_KEY if SUPABASE_KEY and SUPABASE_KEY != "your_supabase_anon_key_here" else None
        
        # If not hardcoded, try .env file
        if not url or not key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                url = os.getenv("SUPABASE_URL")
                key = os.getenv("SUPABASE_KEY")
            except:
                pass
        
        if not url or not key:
            print("Warning: Supabase credentials not found. Running in offline mode.")
            self.client = None
        else:
            try:
                self.client: Client = create_client(url, key)
            except Exception as e:
                print(f"Warning: Could not connect to Supabase: {e}")
                print("Running in offline mode.")
                self.client = None
    
    def is_connected(self):
        """Check if Supabase is configured"""
        return self.client is not None
    
    # Authentication Methods (using Supabase Auth)
    def sign_up_with_email(self, email, password, username):
        """Sign up a new user with email and password"""
        if not self.client:
            return {"success": False, "error": "Database not configured"}
        
        try:
            # Sign up with Supabase Auth
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username
                    }
                }
            })
            
            if auth_response.user:
                # Create user profile in users table
                self.create_user(email, username, 'email')
                return {
                    "success": True,
                    "user": auth_response.user,
                    "session": auth_response.session
                }
            else:
                return {"success": False, "error": "Failed to create user"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sign_in_with_email(self, email, password):
        """Sign in with email and password"""
        if not self.client:
            return {"success": False, "error": "Database not configured"}
        
        try:
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Get user profile
                user_profile = self.get_user_by_email(email)
                return {
                    "success": True,
                    "user": auth_response.user,
                    "session": auth_response.session,
                    "profile": user_profile
                }
            else:
                return {"success": False, "error": "Invalid credentials"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sign_in_with_google(self):
        """Sign in with Google OAuth (returns auth URL)"""
        if not self.client:
            return {"success": False, "error": "Database not configured"}
        
        try:
            # This returns a URL for OAuth authentication
            response = self.client.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": "http://localhost:8080/auth/callback"
                }
            })
            
            return {
                "success": True,
                "url": response.url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def exchange_code_for_session(self, code):
        """Exchange OAuth code for session"""
        if not self.client:
            return {"success": False, "error": "Database not configured"}
        
        try:
            # Exchange the code for a session
            # The new Supabase SDK expects a dict with auth_code
            print(f"Calling exchange_code_for_session with code: {code}")
            
            # Try new format first (dict)
            try:
                response = self.client.auth.exchange_code_for_session({
                    "auth_code": code
                })
            except:
                # Fallback to old format (string)
                response = self.client.auth.exchange_code_for_session(code)
            
            print(f"Response type: {type(response)}")
            print(f"Response: {response}")
            
            # Handle response - it might be a dict or an object
            if response:
                # Try to access as object first
                try:
                    user = response.user if hasattr(response, 'user') else None
                    session = response.session if hasattr(response, 'session') else None
                except:
                    # Try as dict
                    user = response.get('user') if isinstance(response, dict) else None
                    session = response.get('session') if isinstance(response, dict) else None
                
                if user:
                    # Get email from user
                    user_email = None
                    if hasattr(user, 'email'):
                        user_email = user.email
                    elif isinstance(user, dict):
                        user_email = user.get('email')
                    
                    print(f"User email: {user_email}")
                    
                    if user_email:
                        # Get the auth user ID
                        auth_user_id = None
                        if hasattr(user, 'id'):
                            auth_user_id = user.id
                        elif isinstance(user, dict):
                            auth_user_id = user.get('id')
                        
                        # Get or create user profile
                        user_profile = self.get_user_by_email(user_email)
                        
                        if not user_profile:
                            # Create profile for OAuth user
                            username = user_email.split('@')[0]
                            print(f"Creating profile for: {username} with auth_user_id: {auth_user_id}")
                            self.create_user(user_email, username, 'google', auth_user_id)
                            user_profile = self.get_user_by_email(user_email)
                        
                        return {
                            "success": True,
                            "user": user,
                            "session": session,
                            "profile": user_profile
                        }
            
            return {"success": False, "error": "Failed to exchange code - no user data"}
            
        except Exception as e:
            import traceback
            print(f"Exception in exchange_code_for_session:")
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def get_session(self):
        """Get current session"""
        if not self.client:
            return None
        
        try:
            session = self.client.auth.get_session()
            return session
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def sign_out(self):
        """Sign out current user"""
        if not self.client:
            return False
        
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            print(f"Error signing out: {e}")
            return False
    
    # User Management
    def create_user(self, email, username, auth_provider='email', auth_user_id=None):
        """Create a new user in the database
        
        Args:
            email: User's email
            username: User's username
            auth_provider: Authentication provider (email, google, etc.)
            auth_user_id: The ID from auth.users (required for proper linking)
        """
        if not self.client:
            return {"success": False, "error": "Database not configured"}
        
        try:
            # Get auth user ID if not provided
            if not auth_user_id:
                user = self.client.auth.get_user()
                if user and hasattr(user, 'user') and user.user:
                    auth_user_id = user.user.id
                else:
                    return {"success": False, "error": "No authenticated user found"}
            
            data = {
                "id": auth_user_id,  # Use the auth.users.id as primary key
                "email": email,
                "username": username,
                "auth_provider": auth_provider,
                "created_at": datetime.utcnow().isoformat(),
                "total_sessions": 0,
                "total_focus_time": 0,
                "total_check_ins": 0
            }
            
            response = self.client.table("users").insert(data).execute()
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_by_email(self, email):
        """Get user by email"""
        if not self.client:
            return None
        
        try:
            response = self.client.table("users").select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user_stats(self, user_id, sessions=0, focus_time=0, check_ins=0):
        """Update user statistics"""
        if not self.client:
            return False
        
        try:
            response = self.client.table("users").select("*").eq("id", user_id).execute()
            if not response.data:
                return False
            
            user = response.data[0]
            
            update_data = {
                "total_sessions": user.get("total_sessions", 0) + sessions,
                "total_focus_time": user.get("total_focus_time", 0) + focus_time,
                "total_check_ins": user.get("total_check_ins", 0) + check_ins,
                "last_active": datetime.utcnow().isoformat()
            }
            
            self.client.table("users").update(update_data).eq("id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating stats: {e}")
            return False
    
    # Session Management
    def create_session(self, user_id):
        """Create a new focus session"""
        if not self.client:
            return None
        
        try:
            data = {
                "user_id": user_id,
                "start_time": datetime.utcnow().isoformat(),
                "check_ins_count": 0,
                "status": "active"
            }
            
            response = self.client.table("sessions").insert(data).execute()
            return response.data[0]["id"] if response.data else None
        except Exception as e:
            print(f"Error creating session: {e}")
            return None
    
    def end_session(self, session_id):
        """End a focus session"""
        if not self.client:
            return False
        
        try:
            update_data = {
                "end_time": datetime.utcnow().isoformat(),
                "status": "completed"
            }
            
            self.client.table("sessions").update(update_data).eq("id", session_id).execute()
            return True
        except Exception as e:
            print(f"Error ending session: {e}")
            return False
    
    def increment_check_ins(self, session_id):
        """Increment check-in count for a session"""
        if not self.client:
            return False
        
        try:
            response = self.client.table("sessions").select("check_ins_count").eq("id", session_id).execute()
            if not response.data:
                return False
            
            current_count = response.data[0].get("check_ins_count", 0)
            
            self.client.table("sessions").update({
                "check_ins_count": current_count + 1
            }).eq("id", session_id).execute()
            
            return True
        except Exception as e:
            print(f"Error incrementing check-ins: {e}")
            return False
    
    def get_user_sessions(self, user_id, limit=10):
        """Get recent sessions for a user"""
        if not self.client:
            return []
        
        try:
            response = self.client.table("sessions").select("*").eq("user_id", user_id).order("start_time", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []

# Singleton instance
_supabase_client = None

def get_supabase_client():
    """Get or create Supabase client singleton"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client

