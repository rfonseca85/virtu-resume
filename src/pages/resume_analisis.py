import streamlit as st
import sqlite3
from openai import OpenAI
import json

response_json = """
{
    "improvements": [
        {
            "content": "Improvement content"
        }
    ]
}
"""

# Create a connection to SQLite database
conn = sqlite3.connect('virtu_resume.db')
c = conn.cursor()

# Streamlit UI
def main():
    st.title('Resume Analysis')

    # Retrieve resume from the database
    resume_text = get_resume_text(st.session_state["username"])
    # if resume_text:
    #     st.write("Retrieved Resume:")
    #     st.write(resume_text)

    # Button to generate cover letter
    if st.button("Generate Analisis"):
        # Call OpenAI's GPT-3 to generate cover letter
        improvements_json = generate_analisis(resume_text)
            
        # Display generated cover letter
        st.success("Analisis generated successfully.")
            

        display_list_of_improvements(improvements_json)

# Function to retrieve resume text from SQLite database
def get_resume_text(username):
    c.execute("SELECT content FROM resumes where username = ?", (username,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to call OpenAI's GPT-3 and generate cover letter
def generate_analisis(resume_text):

    role = f"""You are resume analist, you write resumes very well. 
    You have to make an analisis of the resume and give some feedback to the user.
    And this is your resume your are analising: {resume_text}"""

    prompt = f"""With all that information, please geneterate list of improvements for the resume.
    Make it look professional.
    Make it unique.
    Dont use the same words from the resume, make it look like a human wrote it.
    Dont use unusual words, make it look like a human wrote it.

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


def display_list_of_improvements(improvements_json):
    

    # Convert the JSON string to a Python dictionary
    improvements_data = json.loads(improvements_json)

    # Start building the Streamlit app
    st.write("---")
    st.subheader("Resume Improvements")

    for improvement in improvements_data['improvements']: 
        st.markdown(
            f"""
            - {improvement['content']}
            """ 
        )
 