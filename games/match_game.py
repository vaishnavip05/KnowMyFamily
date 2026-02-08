import streamlit as st
import os

def match_game(family):
    st.subheader("🎮 Match the Name to the Photo")

    if not family:
        st.warning("No family data found")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Names")
        for m in family:
            st.button(m["name"], key=f"name_{m['name']}")

    with col2:
        st.write("### Photos")
        for m in family:
            photo_path = m.get("photo", "")

            # Resolve absolute path
            abs_path = os.path.join(os.getcwd(), photo_path)

            if os.path.exists(abs_path):
                st.image(abs_path, use_column_width=True)
            else:
                st.warning(f"Image not found for {m['name']}")
