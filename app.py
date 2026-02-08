import streamlit as st
import json
import os

from games.meet_my_family import meet_family
from games.find_my_family import find_family
from games.who_is_speaking import who_is_speaking

# ---------- File paths ----------
BASE_DIR = os.path.dirname(__file__)
USERS_FILE = os.path.join(BASE_DIR, "users.json")

# ---------- Load users ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)["users"]

# ---------- Save users ----------
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2)

# ---------- Authentication ----------
def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

# ---------- Register ----------
def register_user(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return False  # user already exists

    users.append({
        "username": username,
        "password": password
    })
    save_users(users)
    return True

# ---------- Session ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:

    st.title("🔐 Know My Family")

    if st.session_state.page == "login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        if st.button("Create new account"):
            st.session_state.page = "register"
            st.rerun()

    # ---------- REGISTER PAGE ----------
    else:
        st.subheader("Register")

        new_username = st.text_input("Choose Username")
        new_password = st.text_input("Choose Password", type="password")

        if st.button("Register"):
            if new_username and new_password:
                if register_user(new_username, new_password):
                    st.success("Account created. Please login.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Username already exists")
            else:
                st.warning("Fill all fields")

        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# ---------- MAIN APP ----------
else:
    st.title("Know My Family")
    st.write("Choose a game:")

    if st.button("Meet My Family"):
        st.text(meet_family())

    if st.button("Find My Family"):
        q, a = find_family()
        st.write(q)
        st.success(f"Answer: {a}")

    if st.button("Who Is Speaking"):
        audio, a = who_is_speaking()
        st.write(f"Audio file: {audio}")
        st.success(f"Answer: {a}")

    st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()
