"""
Authentication Module - Login
Handles user login with password validation
"""

import streamlit as st
from database.models import User
from database.db import get_session
import hashlib

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def show_login():
    """Display login form and handle authentication"""
    
    # Center the form with custom styling
    st.markdown("""
        <style>
        .login-container {
            max-width: 350px;
            margin: 20px auto 80px auto;
            padding: 10px 10px;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .login-header {
            text-align: center;
            color: white;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 30px;
        }
        div[data-testid="stForm"] {
            border: none;
            padding: 0;
        }
        </style>
        <div class="login-container">
            <div class="login-header">🔐 Login to Skill Gap AI</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create centered columns for compact form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="your.email@example.com", label_visibility="collapsed")
            st.markdown('<p style="color: #94a3b8; font-size: 0.75rem; margin-top: -10px;">📧 Email</p>', unsafe_allow_html=True)
            
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            st.markdown('<p style="color: #94a3b8; font-size: 0.75rem; margin-top: -10px; margin-bottom: 20px;">🔒 Password</p>', unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if not email or not password:
                    st.error("❌ Please fill in all fields!")
                    return
                
                # Validate email format
                if '@' not in email or '.' not in email:
                    st.error("❌ Please enter a valid email address!")
                    return
                
                # Check credentials
                session = get_session()
                try:
                    user = session.query(User).filter_by(email=email.lower()).first()
                    
                    if user and user.password == hash_password(password):
                        # Login successful
                        st.session_state.logged_in = True
                        st.session_state.user_email = user.email
                        st.session_state.user_name = user.name
                        st.success(f"✅ Welcome back, {user.name}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password!")
                except Exception as e:
                    st.error(f"❌ Login failed: {str(e)}")
                finally:
                    session.close()
        
        st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 20px;">💡 Don\'t have an account? Switch to the Register tab!</p>', unsafe_allow_html=True)