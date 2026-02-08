import streamlit as st
import os

def match_game(family):
    st.subheader("🎮 Match the Name to the Photo")

    if not family:
        st.info("No family members found")
        return

    # Layout exactly like old version
    names_col, photos_col = st.columns([1, 2])

    # ---------- LEFT SIDE: NAMES ----------
    with names_col:
        st.markdown("### Names")
        for member in family:
            st.button(member["name"], key=f"name_{member['name']}")

    # ---------- RIGHT SIDE: PHOTOS ----------
    with photos_col:
        st.markdown("### Photos")

        photo_cols = st.columns(3)  # grid like old UI

        for idx, member in enumerate(family):
            with photo_cols[idx % 3]:
                photo_path = member.get("photo", "")

                abs_path = os.path.join(os.getcwd(), photo_path)

                if os.path.exists(abs_path):
                    st.image(abs_path, use_column_width=True)
                else:
                    st.image(
                        "https://via.placeholder.com/150?text=No+Image",
                        use_column_width=True
                    )

                st.button(
                    "Select Photo",
                    key=f"select_{member['name']}"
                )
