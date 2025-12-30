import streamlit as st
import json
import os
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"

# --------------------------------------------------
# Ensure folders exist
# --------------------------------------------------
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# --------------------------------------------------
# Load existing family data
# --------------------------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# --------------------------------------------------
# Save family data
# --------------------------------------------------
def save_family_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --------------------------------------------------
# Family Setup Screen
# --------------------------------------------------
def family_setup_screen(go_to):

    st.title("👨‍👩‍👧 Family Setup (Parent Section)")
    st.write("Please add family members before starting the games.")
    st.markdown("---")

    # Initialize session state list
    if "family_members" not in st.session_state:
        st.session_state.family_members = load_family_data()

    # -------------------------------
    # Input Form
    # -------------------------------
    with st.form("add_member_form"):
        name = st.text_input("Name")
        relationship = st.selectbox(
            "Relationship",
            ["Mother", "Father", "Grandmother", "Grandfather", "Sibling", "Other"]
        )
        image_file = st.file_uploader(
            "Upload Photo",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button("Add Person")

        if submitted:
            if not name or not image_file:
                st.warning("Please enter name and upload photo.")
            else:
                image_path = os.path.join(IMAGE_FOLDER, image_file.name)

                # Save image
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())

                # Add to list
                st.session_state.family_members.append({
                    "name": name,
                    "relationship": relationship,
                    "image": image_file.name
                })

                save_family_data(st.session_state.family_members)
                st.success(f"{name} added successfully!")

    st.markdown("---")

    # -------------------------------
    # Display Added Members
    # -------------------------------
    if st.session_state.family_members:
        st.subheader("Added Family Members")

        cols = st.columns(3)
        for idx, member in enumerate(st.session_state.family_members):
            with cols[idx % 3]:
                img_path = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), width=150)
                st.write(f"**{member['name']}**")
                st.write(member["relationship"])

    st.markdown("---")

    # -------------------------------
    # Finish Setup
    # -------------------------------
    if st.session_state.family_members:
        if st.button("✅ Finish Setup"):
            go_to("home")

