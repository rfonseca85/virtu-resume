import streamlit as st
import sqlite3
import fitz


# Create a connection to SQLite database
conn = sqlite3.connect('./virtu_resume.db')
c = conn.cursor()

# def delete_all_resumes():
#     c.execute("DELETE FROM resumes")
#     conn.commit()

# Function to insert resume into the database
def insert_resume(username, name, content):
    c.execute("INSERT INTO resumes (username, name, content) VALUES (?, ?, ?)", (username, name, content,))
    conn.commit()

# Function to retrieve all resumes from the database
def get_resume(username):
    c.execute("SELECT * FROM resumes where username = ?", (username,))
    return c.fetchall()

# Streamlit UI
def main():
    st.title('Resume')
    username = st.session_state["username"]
    
    # Upload a file
    uploaded_file = st.file_uploader("", type=['pdf'])

    if uploaded_file is not None:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            # Save resume to the database
            insert_resume(username, uploaded_file.name, pdf_text)
            st.success("Resume saved successfully!")
        else:
            st.error("Failed to extract text from the uploaded PDF.")

    # Show all resumes in the database
    resumes = get_resume(username)
    if resumes:
        for resume in resumes:
            st.write("---")
            st.subheader(resume[2],)  # Display resume names
            st.write(resume[3])  # Display resume content

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_text = ''
        pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
        for page in pdf_document:
            pdf_text += page.get_text()
        return pdf_text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

