import streamlit as st
import json
import os
import random
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"


def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def find_my_family_screen(go_to):

    st.title("🛤️ Find My Family")
    st.markdown("---")

    family = load_family_data()
    if len(family) < 2:
        st.warning("Please add at least 2 family members.")
        if st.button("⬅ Back"):
            go_to("setup")
        return

    # -------------------------------
    # STATE INIT
    # -------------------------------
    if "fm_stage" not in st.session_state:
        st.session_state.fm_stage = "intro"

    # -------------------------------
    # STAGE 1: SHOW FAMILY
    # -------------------------------
    if st.session_state.fm_stage == "intro":
        st.subheader("👨‍👩‍👧 My Family")

        cols = st.columns(3)
        for i, m in enumerate(family):
            with cols[i % 3]:
                img = os.path.join(IMAGE_FOLDER, m["image"])
                if os.path.exists(img):
                    st.image(Image.open(img), width=140)
                st.write(f"**{m['name']}**")
                st.write(m["relationship"])

        if st.button("▶ Start Game"):
            st.session_state.fm_stage = "game"
            st.rerun()

        if st.button("⬅ Back to Home"):
            go_to("home")
        return

    # -------------------------------
    # STAGE 2: GAME SETUP
    # -------------------------------
    if "graph" not in st.session_state:
        target = random.choice(family)
        wrong = random.choice([m for m in family if m != target])

        st.session_state.target = target
        st.session_state.wrong = wrong

        # Node graph
        # 0 = start
        # Correct path: 0 → 1 → 2 → 3 → 4
        st.session_state.graph = {
            0: [1, 5],
            1: [2, 6],
            2: [3],
            3: [4],
            4: ["target", "wrong"]
        }

        st.session_state.current = 0
        st.session_state.visited = [0]

    target = st.session_state.target
    wrong = st.session_state.wrong

    st.info(f"🧒 Task: Give the 🍎 apple to **{target['relationship']} ({target['name']})**")
    st.markdown("---")

    # -------------------------------
    # DRAW PATH
    # -------------------------------
    st.subheader("🧭 Choose your path")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        for node in range(5):
            if node in st.session_state.visited:
                st.markdown("🟢")
            else:
                st.markdown("⚪")

            if node in st.session_state.graph and node == st.session_state.current:
                for nxt in st.session_state.graph[node]:
                    if isinstance(nxt, int):
                        if st.button(f"➡ Node {nxt}", key=f"n{node}_{nxt}"):
                            if nxt == node + 1:
                                st.session_state.visited.append(nxt)
                                st.session_state.current = nxt
                                st.success("Good choice!")
                            else:
                                st.warning("Try again 🙂")
                            st.rerun()

    # -------------------------------
    # FINAL CHOICE
    # -------------------------------
    if st.session_state.current == 4:
        st.markdown("---")
        st.subheader("🔀 Who should get the apple?")

        c1, c2 = st.columns(2)

        with c1:
            img = os.path.join(IMAGE_FOLDER, target["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=150)
            if st.button(f"Give to {target['name']}"):
                st.balloons()
                st.success("🎉 Correct! Well done!")
                reset_find_my_family()

        with c2:
            img = os.path.join(IMAGE_FOLDER, wrong["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=150)
            if st.button(f"Give to {wrong['name']}"):
                st.error("❌ Oops! Try again 🙂")

    if st.button("⬅ Back to Home"):
        reset_find_my_family()
        go_to("home")


def reset_find_my_family():
    for k in [
        "fm_stage",
        "graph",
        "current",
        "visited",
        "target",
        "wrong",
    ]:
        if k in st.session_state:
            del st.session_state[k]
