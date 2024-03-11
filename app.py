import streamlit as st
from streamlit_extras.badges import badge
import src.pages.menu as menu
import user_management as user_management


# Return the selected Page content
st.set_page_config(
    page_title="Virtu.resume",
    page_icon="🔎",
    initial_sidebar_state="expanded",
)

authenticator = user_management.login()

if st.session_state["authentication_status"]:
    menu.main(authenticator)

    with st.sidebar:
        st.write("")
        st.write("")
        badge(type="buymeacoffee", name="rfonseca85")
        badge(type="github", name="rfonseca85/virtu-resume")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

    




