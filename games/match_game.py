import streamlit as st
import random

def match_game(family):
    st.subheader("🎮 Match the Name to the Photo")

    names = [m["name"] for m in family]
    random.shuffle(names)

    cols = st.columns(2)

    with cols[0]:
        st.write("### Names")
        for name in names:
            st.button(name, key=f"name_{name}")

    with cols[1]:
        st.write("### Photos")
        for m in family:
            st.image(m["photo"], use_column_width=True)
