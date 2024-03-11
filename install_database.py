import sqlite3
import streamlit_authenticator as stauth


def main():


  hashed_passwords = stauth.Hasher(['interpol']).generate()
  print(hashed_passwords[0])


  # Create a connection to SQLite database
  conn = sqlite3.connect('virtu_resume.db')
  c = conn.cursor()

  # Create a table to store resumes if it doesn't exist
  c.execute('''CREATE TABLE IF NOT EXISTS resumes
              (id INTEGER PRIMARY KEY, username TEXT, name TEXT, content TEXT)''')
  conn.commit()



if __name__ == "__main__":
  main()