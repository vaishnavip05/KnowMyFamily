import streamlit as st
import json
import os

# ---------------- PATHS ----------------
BASE = os.path.dirname(__file__)
USERS_FILE = os.path.join(BASE, "users.json")
FAMILY_FILE = os.path.join(BASE, "family_data.json")
PHOTO_DIR = os.path.join(BASE, "uploads/photos")
AUDIO_DIR = os.path.join(BASE, "uploads/audio")

os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ---------------- DATA HELPERS ----------------
def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)["users"]

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2)

def authenticate(u, p):
    return any(x["username"] == u and x["password"] == p for x in load_users())

def register_user(u, p):
    users = load_users()
    users.append({"username": u, "password": p})
    save_users(users)

def load_family():
    with open(FAMILY_FILE) as f:
        return json.load(f)["family"]

def save_family(family):
    with open(FAMILY_FILE, "w") as f:
        json.dump({"family": family}, f, indent=2)

# ---------------- SESSION ----------------
st.session_state.setdefault("page", "login")
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("user", None)

# ================= LOGIN PAGE =================
if not st.session_state.logged_in:
    st.title("🔐 Know My Family")

    if st.session_state.page == "login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(u, p):
                st.session_state.logged_in = True
                st.session_state.user = u
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Invalid login")

        if st.button("Create Account"):
            st.session_state.page = "register"
            st.rerun()

    else:
        u = st.text_input("Choose Username")
        p = st.text_input("Choose Password", type="password")

        if st.button("Register"):
            register_user(u, p)
            st.success("Account created")
            st.session_state.page = "login"
            st.rerun()

# ================= HOME DASHBOARD =================
elif st.session_state.page == "home":
    st.title(f"👨‍👩‍👧 Welcome, {st.session_state.user}")

    if st.button("Know My Family"):
        st.session_state.page = "family"
        st.rerun()

    if st.button("Parent Section"):
        st.session_state.page = "parent"
        st.rerun()

    if st.button("Games"):
        st.session_state.page = "game"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# ================= KNOW MY FAMILY =================
elif st.session_state.page == "family":
    st.title("👨‍👩‍👧 Know My Family")
    family = load_family()

    cols = st.columns(3)
    for i, m in enumerate(family):
        with cols[i % 3]:
            st.image(m["photo"], use_column_width=True)
            st.write(f"**{m['name']}**")
            st.caption(m["relation"])
            st.audio(m["audio"])

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ================= PARENT SECTION =================
elif st.session_state.page == "parent":
    st.title("👨‍👩‍👧 Family Setup (Parent Section)")

    name = st.text_input("Name")
    relation = st.text_input("Relationship")
    photo = st.file_uploader("Upload Photo", ["jpg","png"])
    audio = st.file_uploader("Upload Voice", ["mp3","wav"])

    if st.button("Add Person"):
        photo_path = f"uploads/photos/{photo.name}"
        audio_path = f"uploads/audio/{audio.name}"

        with open(os.path.join(BASE, photo_path), "wb") as f:
            f.write(photo.getbuffer())
        with open(os.path.join(BASE, audio_path), "wb") as f:
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
        st.rerun()

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ================= GAMES =================
elif st.session_state.page == "game":
    st.title("🎮 Match the Name to the Photo")
    family = load_family()

    left, right = st.columns([1, 2])

    with left:
        st.subheader("Names")
        for m in family:
            st.button(m["name"])

    with right:
        st.subheader("Photos")
        cols = st.columns(3)
        for i, m in enumerate(family):
            with cols[i % 3]:
                st.image(m["photo"], use_column_width=True)
                st.button("Select Photo")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

