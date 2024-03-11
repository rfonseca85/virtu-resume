import streamlit as st
import streamlit_authenticator as stauth
import yaml

# hashed_passwords = stauth.Hasher(['interpol']).generate()
# print(hashed_passwords[0])

from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

def login():

  authenticator = stauth.Authenticate(
      config['credentials'],
      config['cookie']['name'],
      config['cookie']['key'],
      config['cookie']['expiry_days'],
      config['preauthorized']
  )

  authenticator.login()

  return authenticator

def user_settings(authenticator):
  st.title('User Management')
  
  if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

    except Exception as e:
        st.error(e)
  
  authenticator.logout()