"""
Authentication Module - Registration
Handles new user registration with validation
"""

import streamlit as st
from database.models import User
from database.db import get_session
import hashlib
import re

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def show_register():
    """Display registration form and handle user creation"""
    
    # Center the form with custom styling
    st.markdown("""
        <style>
        .register-container {
            max-width: 350px;
            margin: 20px auto 80px auto;
            padding: 10px;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .register-header {
            text-align: center;
            color: white;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 30px;
        }
        </style>
        <div class="register-container">
            <div class="register-header">📝 Create Your Account</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create centered columns for compact form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            name = st.text_input("👤 Full Name", placeholder="John Doe", label_visibility="collapsed")
            st.markdown('<p style="color: #94a3b8; font-size: 0.75rem; margin-top: -10px;">👤 Full Name</p>', unsafe_allow_html=True)
            
            email = st.text_input("📧 Email", placeholder="your.email@example.com", label_visibility="collapsed")
            st.markdown('<p style="color: #94a3b8; font-size: 0.75rem; margin-top: -10px;">📧 Email</p>', unsafe_allow_html=True)
            
            password = st.text_input("🔒 Password", type="password", placeholder="Min 6 chars, letters & numbers", label_visibility="collapsed")
            st.markdown('<p style="color: #94a3b8; font-size: 0.75rem; margin-top: -10px;">🔒 Password</p>', unsafe_allow_html=True)
            
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password", label_visibility="collapsed")
            st.markdown('<p style="color: #94a3b8; font-size: 0.75rem; margin-top: -10px; margin-bottom: 20px;">🔒 Confirm Password</p>', unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("Register", use_container_width=True)
            
            if submit_button:
                # Validation
                if not name or not email or not password or not confirm_password:
                    st.error("❌ Please fill in all fields!")
                    return
                
                if not validate_email(email):
                    st.error("❌ Please enter a valid email address!")
                    return
                
                if password != confirm_password:
                    st.error("❌ Passwords do not match!")
                    return
                
                is_valid, message = validate_password(password)
                if not is_valid:
                    st.error(f"❌ {message}")
                    return
                
                # Create user
                session = get_session()
                try:
                    # Check if user already exists
                    existing_user = session.query(User).filter_by(email=email.lower()).first()
                    if existing_user:
                        st.error("❌ An account with this email already exists!")
                        return
                    
                    # Create new user
                    new_user = User(
                        name=name,
                        email=email.lower(),
                        password=hash_password(password)
                    )
                    session.add(new_user)
                    session.commit()
                    
                    st.success(f"✅ Account created successfully! Welcome, {name}!")
                    st.info("👉 Please switch to the Login tab to sign in.")
                    
                except Exception as e:
                    session.rollback()
                    st.error(f"❌ Registration failed: {str(e)}")
                finally:
                    session.close()
        
        st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 20px;">💡 Already have an account? Switch to the Login tab!</p>', unsafe_allow_html=True)