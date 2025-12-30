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
# Find My Family – NODE PATH GAME
# --------------------------------------------------
def find_my_family_screen(go_to):

    st.title("🛤️ Find My Family")
    st.write("Help the child walk step-by-step to the right family member 💙")
    st.markdown("---")

    family = load_family_data()

    if len(family) < 2:
        st.warning("Please add at least 2 family members first.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # --------------------------------------------------
    # INITIALIZE GAME
    # --------------------------------------------------
    if "path_game" not in st.session_state:
        target = random.choice(family)
        wrong = random.choice([m for m in family if m != target])

        st.session_state.path_game = {
            "target": target,
            "wrong": wrong,
            "current": 0,
            "completed": []
        }

    game = st.session_state.path_game
    target = game["target"]
    wrong = game["wrong"]

    # --------------------------------------------------
    # TASK
    # --------------------------------------------------
    st.info(f"🧒 Task: Give the 🍎 apple to **{target['relationship']} ({target['name']})**")
    st.markdown("---")

    # --------------------------------------------------
    # DEFINE NODES
    # --------------------------------------------------
    # Correct path = 0 → 1 → 2 → 3 → 4
    correct_nodes = [0, 1, 2, 3, 4]
    wrong_nodes = [5, 6]

    # --------------------------------------------------
    # PATH VISUALIZATION
    # --------------------------------------------------
    st.subheader("🚶 Walking Path")

    path_display = ""
    for i in correct_nodes:
        if i in game["completed"]:
            path_display += "🟢━━"
        else:
            path_display += "⚪━━"
    st.markdown(path_display)

    st.markdown("---")

    # --------------------------------------------------
    # NODE SELECTION
    # --------------------------------------------------
    st.subheader("Choose where to go next")

    cols = st.columns(3)

    # Correct next node
    next_correct = game["current"] + 1

    with cols[0]:
        if next_correct <= 4:
            if st.button(f"➡️ Go to Node {next_correct}"):
                game["completed"].append(next_correct)
                game["current"] = next_correct
                st.success("Good choice! 👍")
                st.rerun()

    # Wrong nodes
    with cols[1]:
        if st.button("❌ Wrong Path"):
            st.warning("Oops! That path is blocked. Try again 🙂")

    # --------------------------------------------------
    # FINAL CHOICE
    # --------------------------------------------------
    if game["current"] == 4:
        st.markdown("---")
        st.subheader("🔀 Final Choice")

        col1, col2 = st.columns(2)

        with col1:
            img = os.path.join(IMAGE_FOLDER, target["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=150)
            if st.button(f"Give to {target['name']}"):
                st.balloons()
                st.success("🎉 Correct! You reached the right person!")
                del st.session_state.path_game

        with col2:
            img = os.path.join(IMAGE_FOLDER, wrong["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=150)
            if st.button(f"Give to {wrong['name']}"):
                st.error("❌ Wrong person! Try again 🙂")

    st.markdown("---")
    if st.button("⬅ Back to Home"):
        if "path_game" in st.session_state:
            del st.session_state.path_game
        go_to("home")
