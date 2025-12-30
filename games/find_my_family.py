import streamlit as st

def find_my_family_screen(go_to):
    st.header("🛤️ Find My Family")
    st.write("Follow the path and find the correct family member.")
    st.markdown("---")

    st.info("This game will be implemented next.")

    if st.button("⬅ Back to Home"):
        go_to("home")
