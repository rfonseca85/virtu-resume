import streamlit as st
from streamlit_extras.badges import badge
import src.pages.menu as menu


# Return the selected Page content
st.set_page_config(
    page_title="Virtu.resume",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

menu.page()

with st.sidebar:
    st.write("")
    st.write("")
    badge(type="buymeacoffee", name="rfonseca85")
    badge(type="github", name="rfonseca85/virtu-resume")
    




