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
# Meet My Family Game Screen
# --------------------------------------------------
def meet_my_family_screen(go_to):

    st.title("👨‍👩‍👧 Meet My Family")
    st.write("First, look at your family members. Then play the matching game 💙")
    st.markdown("---")

    family = load_family_data()

    if not family:
        st.warning("No family members found. Please complete Family Setup first.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # --------------------------------------------------
    # Step 1: Familiarization View
    # --------------------------------------------------
    if "start_game" not in st.session_state:
        st.session_state.start_game = False

    if not st.session_state.start_game:
        st.subheader("📸 My Family")

        cols = st.columns(3)
        for idx, member in enumerate(family):
            with cols[idx % 3]:
                img_path = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), width=150)
                st.write(f"**{member['name']}**")
                st.write(member["relationship"])

        st.markdown("---")
        if st.button("▶ Start Game"):
            st.session_state.start_game = True
            st.session_state.selected_name = None
            st.session_state.matched = []
            st.rerun()

        if st.button("⬅ Back to Home"):
            go_to("home")

        return

    # --------------------------------------------------
    # Step 2: Matching Game
    # --------------------------------------------------
    st.subheader("🎮 Match the Name to the Photo")

    # Initialize shuffled data once
    if "shuffled_names" not in st.session_state:
        st.session_state.shuffled_names = random.sample(
            [m["name"] for m in family], len(family)
        )
        st.session_state.shuffled_photos = random.sample(
            family, len(family)
        )

    # Store matches
    if "matched" not in st.session_state:
        st.session_state.matched = []

    if "selected_name" not in st.session_state:
        st.session_state.selected_name = None

    col1, col2 = st.columns(2)

    # -----------------------
    # Left: Names
    # -----------------------
    with col1:
        st.markdown("### 🏷 Names")
        for name in st.session_state.shuffled_names:
            if name in st.session_state.matched:
                st.success(name)
            else:
                if st.button(name, key=f"name_{name}"):
                    st.session_state.selected_name = name
                    st.rerun()

    # -----------------------
    # Right: Photos
    # -----------------------
    with col2:
        st.markdown("### 🖼 Photos")

        for member in st.session_state.shuffled_photos:
            img_path = os.path.join(IMAGE_FOLDER, member["image"])
            if os.path.exists(img_path):
                st.image(Image.open(img_path), width=150)

            if member["name"] in st.session_state.matched:
                st.success("Matched ✅")
            else:
                if st.button("Select Photo", key=f"photo_{member['name']}"):
                    if st.session_state.selected_name == member["name"]:
                        st.session_state.matched.append(member["name"])
                        st.session_state.selected_name = None
                        st.success("Correct! 🎉")
                    else:
                        st.warning("Try again 🙂")
                        st.session_state.selected_name = None
                    st.rerun()

    # --------------------------------------------------
    # Completion
    # --------------------------------------------------
    if len(st.session_state.matched) == len(family):
        st.balloons()
        st.success("🎉 Great job! You matched everyone!")

        if st.button("🔁 Play Again"):
            for key in [
                "start_game",
                "shuffled_names",
                "shuffled_photos",
                "matched",
                "selected_name",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.markdown("---")
    if st.button("⬅ Back to Home"):
        for key in [
            "start_game",
            "shuffled_names",
            "shuffled_photos",
            "matched",
            "selected_name",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        go_to("home")

