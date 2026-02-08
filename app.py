import streamlit as st
import json
import os
from games.match_game import match_game

BASE = os.path.dirname(__file__)
USERS_FILE = os.path.join(BASE, "users.json")
FAMILY_FILE = os.path.join(BASE, "family_data.json")

# ---------- UTILITIES ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)["users"]

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2)

def user_exists(username):
    return any(u["username"] == username for u in load_users())

def authenticate(username, password):
    return any(
        u["username"] == username and u["password"] == password
        for u in load_users()
    )

def register_user(username, password):
    users = load_users()
    users.append({
        "username": username,
        "password": password
    })
    save_users(users)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------- LOGIN / REGISTER ----------
if not st.session_state.logged_in:
    st.title("🔐 Know My Family")

    if st.session_state.page == "login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.page = "home"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        if st.button("Create new account"):
            st.session_state.page = "register"
            st.rerun()

    else:
        st.subheader("Register (Create Account)")

        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")

        if st.button("Register"):
            if not new_user or not new_pass:
                st.warning("Fill all fields")
            elif user_exists(new_user):
                st.error("Username already exists")
            else:
                register_user(new_user, new_pass)
                st.success("Account created. Please login.")
                st.session_state.page = "login"
                st.rerun()

        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------- HOME (AFTER LOGIN) ----------
else:
    st.title(f"👨‍👩‍👧 Welcome, {st.session_state.current_user}")

    st.write("Choose a game:")

    if st.button("Start Match Game"):
        st.session_state.page = "game"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.page = "login"
        st.rerun()

# ---------- GAME PAGE ----------
elif st.session_state.logged_in and st.session_state.page == "game":
    family = load_family()          # ✅ LOAD DATA
    match_game(family)              # ✅ PASS DATA

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
