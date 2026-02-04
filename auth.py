import streamlit as st
import json
import os

USERS_FILE = "data/users.json"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Initialize users file
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

# Load users
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# -------------------------------
# AUTH SCREEN
# -------------------------------
def auth_screen():
    st.title("🔐 Welcome to Know My Family")

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign In"):
            st.session_state.auth_mode = "login"

    with col2:
        if st.button("Sign Up"):
            st.session_state.auth_mode = "signup"

    st.markdown("---")

    users = load_users()

    # -------------------------------
    # SIGN UP
    # -------------------------------
    if st.session_state.auth_mode == "signup":
        st.subheader("📝 Create Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            if not username or not password:
                st.warning("Please fill all fields")
            elif username in users:
                st.error("Username already exists")
            else:
                users[username] = password
                save_users(users)
                st.success("Account created! Please sign in.")
                st.session_state.auth_mode = "login"

    # -------------------------------
    # SIGN IN
    # -------------------------------
    else:
        st.subheader("🔑 Sign In")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
