import streamlit as st

def meet_my_family_screen(go_to):
    st.header("👨‍👩‍👧 Meet My Family")
    st.write("Learn the names and relationships of your family members.")
    st.markdown("---")

    st.info("This game will be implemented next.")

    if st.button("⬅ Back to Home"):
        go_to("home")
