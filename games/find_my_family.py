import streamlit as st
import json
import os
import random
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"

# --------------------------------------------------
# Load family data
# --------------------------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


# --------------------------------------------------
# Find My Family Game
# --------------------------------------------------
def find_my_family_screen(go_to):

    st.title("🛤️ Find My Family")
    st.write("Help the child walk and give the correct item to the right family member 💙")
    st.markdown("---")

    family = load_family_data()

    if len(family) < 2:
        st.warning("Please add at least 2 family members in Family Setup.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # -------------------------------
    # STEP 0: INTRO VIEW
    # -------------------------------
    if "find_game_started" not in st.session_state:
        st.subheader("👨‍👩‍👧 My Family")

        cols = st.columns(3)
        for i, member in enumerate(family):
            with cols[i % 3]:
                img_path = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), width=140)
                st.write(f"**{member['name']}**")
                st.write(member["relationship"])

        st.markdown("---")
        if st.button("▶ Start Game"):
            target = random.choice(family)
            wrong = random.choice([m for m in family if m != target])

            st.session_state.find_game_started = True
            st.session_state.target = target
            st.session_state.wrong = wrong
            st.session_state.step = 0
            st.session_state.max_steps = 3
            st.rerun()

        if st.button("⬅ Back to Home"):
            go_to("home")

        return

    # -------------------------------
    # TASK INSTRUCTION
    # -------------------------------
    target = st.session_state.target
    wrong = st.session_state.wrong

    objects = ["☕ coffee", "🥛 milk", "📺 remote", "🍎 apple"]
    task_object = random.choice(objects)

    st.info(f"🧒 Task: **Give the {task_object} to {target['relationship']} ({target['name']})**")

    st.markdown("---")

    # -------------------------------
    # WALKING PATH
    # -------------------------------
    st.subheader("🚶 Walking Path")

    st.write(f"Current position: Step **{st.session_state.step}** of {st.session_state.max_steps}")
    st.write("🧒")

    if st.session_state.step < st.session_state.max_steps:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("➡️ Move Forward"):
                st.session_state.step += 1
                st.rerun()

        with col2:
            if st.button("❌ Wrong Turn"):
                st.warning("Oops! That path is blocked. Try again 🙂")

        return

    # -------------------------------
    # FINAL CHOICE
    # -------------------------------
    st.markdown("---")
    st.subheader("🔀 Final Choice")

    col1, col2 = st.columns(2)

    with col1:
        img = os.path.join(IMAGE_FOLDER, target["image"])
        if os.path.exists(img):
            st.image(Image.open(img), width=150)
        if st.button(f"Give to {target['name']}"):
            st.success("🎉 Correct! You reached the right person!")
            st.balloons()
            st.session_state.find_game_started = False

    with col2:
        img = os.path.join(IMAGE_FOLDER, wrong["image"])
        if os.path.exists(img):
            st.image(Image.open(img), width=150)
        if st.button(f"Give to {wrong['name']}"):
            st.error("❌ Wrong person! Try again 🙂")

    st.markdown("---")
    if st.button("⬅ Back to Home"):
        st.session_state.find_game_started = False
        go_to("home")
