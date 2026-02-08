import streamlit as st

from games.meet_my_family import meet_family
from games.find_my_family import find_family
from games.who_is_speaking import who_is_speaking

st.title("Know My Family")

st.write("Choose a game:")

if st.button("Meet My Family"):
    result = meet_family()
    st.text(result)

if st.button("Find My Family"):
    question, answer = find_family()
    st.write(question)
    st.success(f"Answer: {answer}")

if st.button("Who Is Speaking"):
    audio, answer = who_is_speaking()
    st.write(f"Audio file: {audio}")
    st.success(f"Answer: {answer}")
