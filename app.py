import streamlit as st
import json
import os
from games.match_game import match_game

BASE = os.path.dirname(__file__)
FAMILY_FILE = os.path.join(BASE, "family_data.json")
USERS_FILE = os.path.join(BASE, "users.json")
PHOTO_DIR = os.path.join(BASE, "uploads/photos")
AUDIO_DIR = os.path.join(BASE, "uploads/audio")

os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ---------------- LOAD DATA ----------------
def load_family():
    with open(FAMILY_FILE, "r") as f:
        return json.load(f)["family"]

def save_family(data):
    with open(FAMILY_FILE, "w") as f:
        json.dump({"family": data}, f, indent=2)

def authenticate(u, p):
    with open(USERS_FILE) as f:
        users = json.load(f)["users"]
    return any(x["username"] == u and x["password"] == p for x in users)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🔐 Know My Family – Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(u, p):
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- HOME PAGE ----------------
elif st.session_state.page == "home":
    st.title("👨‍👩‍👧 Family Members")

    family = load_family()
    cols = st.columns(3)

    for i, m in enumerate(family):
        with cols[i % 3]:
            st.image(m["photo"], use_column_width=True)
            st.write(f"**{m['name']}**")
            st.caption(m["relation"])
            st.audio(m["audio"])
            if st.button("Delete", key=m["name"]):
                family.remove(m)
                save_family(family)
                st.rerun()

    st.divider()
    if st.button("Start Game"):
        st.session_state.page = "game"
        st.rerun()

    if st.button("Parent Setup"):
        st.session_state.page = "parent"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# ---------------- PARENT SETUP ----------------
elif st.session_state.page == "parent":
    st.title("👨‍👩‍👧 Family Setup (Parent Section)")

    name = st.text_input("Name")
    relation = st.text_input("Relationship")
    photo = st.file_uploader("Upload Photo", ["jpg","png"])
    audio = st.file_uploader("Upload Voice", ["mp3","wav"])

    if st.button("Add Person"):
        if name and relation and photo and audio:
            photo_path = f"uploads/photos/{photo.name}"
            audio_path = f"uploads/audio/{audio.name}"

            with open(photo_path, "wb") as f:
                f.write(photo.getbuffer())
            with open(audio_path, "wb") as f:
                f.write(audio.getbuffer())

            family = load_family()
            family.append({
                "name": name,
                "relation": relation,
                "photo": photo_path,
                "audio": audio_path
            })
            save_family(family)
            st.success("Member added")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- GAME PAGE ----------------
elif st.session_state.page == "game":
    family = load_family()
    match_game(family)

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()
