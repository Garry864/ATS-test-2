import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import os
import base64
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit settings
page_title = "Smart ATS"
page_icon = ":pager:"
page2 = ":desktop_computer:"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(f"{page_title} {page2}")
st.markdown("Improve Your Resume with ATS")

# Initialize session state variables
if "resume_analysis_response" not in st.session_state:
    st.session_state.resume_analysis_response = None

if "percentage_match_response" not in st.session_state:
    st.session_state.percentage_match_response = None

if "improvisation_response" not in st.session_state:
    st.session_state.improvisation_response = None

# Sidebar for file upload
st.sidebar.title("Upload Your Resume 👇")
uploaded_file = st.sidebar.file_uploader("Upload PDF File", type="pdf", help="Please upload your resume in PDF format")


# Function to get Gemini AI response
def get_gemini_response(input):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


# Function to display the uploaded PDF
def show_pdf(uploaded_file):
    pdf_contents = uploaded_file.read()
    base64_pdf = base64.b64encode(pdf_contents).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Prompt templates
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. Start with the name and job profile of the candidate.
resume:{text}
description:{jd}
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords missing, and finally, final thoughts.
resume:{text}
description:{jd}
"""

input_prompt3 = """
Consider yourself as an ATS advisor for the application. Give the best possible improvisation suggestions from the response and form the resume and the job description. check wether the candidate is experienced or fresher then Highlight the skillsets which needs to be improved according to the description also tell the candidate where he/she focus more on skillsets. and most important start with the phrase listen candidate name with its proper name if specified in the resume.
resume:{text}
description:{jd}
response:{response}
"""

# Layout for job description input
input_text = st.text_area("Job Description:", key="input", height=200)

# Option menu for analysis types
selected = option_menu(
    menu_title=None,
    options=["Resume Analysis", "Percentage Match", "Improvisation"],
    icons=["file-earmark-pdf", "percent", "lightbulb"],
    orientation="horizontal"
)

# Perform actions based on selected menu item
if uploaded_file is not None:
    show_pdf(uploaded_file)
    pdf_content = input_pdf_text(uploaded_file)
    input_data = {
                "text": pdf_content,
                "jd": input_text
            }
    
    if selected == "Resume Analysis":
        with st.expander("About this resume ⤵"):
            if st.session_state.resume_analysis_response is None:
                with st.spinner('Processing...'):
                    response = get_gemini_response(input_prompt1.format(**input_data))
                if response:
                    st.session_state.resume_analysis_response = response
                    st.subheader("Resume Analysis")
                    st.write(response)
            else:
                st.write(st.session_state.resume_analysis_response)

    elif selected == "Percentage Match":
        with st.expander("ATS Score of this Resume ⤵"):
            if st.session_state.percentage_match_response is None:
                with st.spinner('Processing...'):
                    response = get_gemini_response(input_prompt2.format(**input_data))
                if response:
                    st.session_state.percentage_match_response = response
                    st.subheader("Percentage Match")
                    st.write(response)
            else:
                st.write(st.session_state.percentage_match_response)

    elif selected == "Improvisation":
        with st.expander("Suggestions for your Improvisation here ⤵"):
            if st.session_state.improvisation_response is None:
                if st.session_state.percentage_match_response:
                    
                        pdf_content = input_pdf_text(uploaded_file)
                        response_data = {
                            "text": pdf_content,
                            "jd": input_text,
                            "response": st.session_state.percentage_match_response
                        }
                        with st.spinner('Processing...'):
                            response = get_gemini_response(input_prompt3.format(**response_data))
                        if response:
                            st.subheader("Improvisation Suggestions")
                            st.write(response)
                            st.session_state.improvisation_response = response
                else:
                    st.warning("Please complete the 'Percentage Match' analysis first.")
            else:
                st.write(st.session_state.improvisation_response)

else:
    st.warning("Please upload the resume")

# Download links
if st.session_state.resume_analysis_response:
    st.sidebar.download_button(
        label="Download Resume Analysis",
        data=st.session_state.resume_analysis_response,
        file_name="resume_analysis.txt"
    )

if st.session_state.percentage_match_response:
    st.sidebar.download_button(
        label="Download Percentage Match",
        data=st.session_state.percentage_match_response,
        file_name="percentage_match.txt"
    )

if st.session_state.improvisation_response:
    st.sidebar.download_button(
        label="Download Improvisation Suggestions",
        data=st.session_state.improvisation_response,
        file_name="improvisation_suggestions.txt"
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.text("Built with ❤️ by Gaurav Yadav")