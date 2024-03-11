import streamlit as st
import sqlite3
from openai import OpenAI
import json

response_json = """
    {
        "applicant": {
            "name": "Applicant's Name",
            "address": "Applicant's Address",
            "phone": "Applicant's Phone Number",
            "email": "Applicant's Email"
        },
        "recipient": {
            "company": "Company Name"
        },
        "date": "Date",
        "content": {
            "body": "Cover Letter Content",
            "signature": "Applicant's Signature (optional)"
        }
    }
"""

# Create a connection to SQLite database
conn = sqlite3.connect('virtu_resume.db')
c = conn.cursor()

# Streamlit UI
def main():
    st.title('Cover Letter')

    # Input fields for job description
    company_name = st.text_input("Company Name")
    job_title = st.text_input("Job Title")
    description = st.text_area("Job Description")

    # Retrieve resume from the database
    resume_text = get_resume_text(st.session_state["username"])
    # if resume_text:
    #     st.write("Retrieved Resume:")
    #     st.write(resume_text)

    # Button to generate cover letter
    if st.button("Generate Cover Letter"):
        if company_name and job_title and description:
            # Call OpenAI's GPT-3 to generate cover letter
            cover_letter_json = generate_cover_letter(company_name, job_title, description, resume_text)
            
            # Display generated cover letter
            st.success("Cover Letter Generated Successfully!")
            

            display_cover_letter(cover_letter_json)
        else:
            st.error("Please fill in all fields.")

# Function to retrieve resume text from SQLite database
def get_resume_text(username):
    c.execute("SELECT content FROM resumes where username = ?", (username,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to call OpenAI's GPT-3 and generate cover letter
def generate_cover_letter(company_name, job_title, description, resume_text):

    role = f"""You are applying for the position of {job_title} at {company_name}. 
    Here is the description of the job: {description}.
    And this is your resume Your resume: {resume_text}"""

    prompt = f"""With all that information, please geneterate a cover letter crossing the information, write a cover letter for this job application. also research the company and include a sentence about what would excites me to work on this company.
    Make it look professional.
    Make it unique.
    Dont use the same words from the resume, make it look like a human wrote it.
    Dont use unusual words, make it look like a human wrote it.

    Use the current date for the cover letter and dont need to mention the company address, just the company name.
    
    Return it in a json format like this:
    {response_json}
    """

    model = OpenAI()
    model.timeout = 30
    messages = [
        {
            "role": "system",
            "content": role,
        },
        {
            "role": "user",
            "content": prompt,
        }
    ]

    response = model.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        max_tokens=1024,
        stop=None,
        temperature=0.7,
    )

    # Properly accessing the generated text from the ChatCompletionMessage object
    if response.choices and len(response.choices) > 0:
        # Assuming the first choice contains the response we're interested in
        first_choice = response.choices[0]
        if hasattr(first_choice, 'message') and first_choice.message:
            generated_response = first_choice.message.content
        else:
            generated_response = None
    else:
        generated_response = None

    return generated_response.strip() if generated_response else "Failed to generate cover letter."


def display_cover_letter(cover_letter):
    
  # Convert the JSON string to a Python dictionary
    cover_letter_data = json.loads(cover_letter)

    # Start building the Streamlit app
    # st.title("Cover Letter")

    # # Applicant Information
    # st.subheader("Applicant Information")
    # st.write(f"**Name:** {cover_letter_data['applicant']['name']}")
    # st.write(f"**Address:** {cover_letter_data['applicant']['address']}")
    # st.write(f"**Phone:** {cover_letter_data['applicant']['phone']}")
    # st.write(f"**Email:** {cover_letter_data['applicant']['email']}")

    st.write("---")

    # # Recipient Information
    # st.subheader("Recipient")
    # st.write(f"**Company:** {cover_letter_data['recipient']['company']}")

    # st.write("---")

    # # Date
    # st.write(f"**Date:** {cover_letter_data['date']}")

    # Cover Letter Body
    st.subheader("Cover Letter")
    st.write(cover_letter_data['content']['body'])

    # # Signature
    # if cover_letter_data['content'].get('signature'):
    #     st.write("---")
    #     st.write(f"**Signature:** {cover_letter_data['content']['signature']}")
 

