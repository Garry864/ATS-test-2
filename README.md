# Smart ATS :pager::desktop_computer:

![Smart ATS](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQx8PoA0ZmpCt7R3P7SbHcljKZ04Wft7QoX9C-GqjUS_IKMDzf9tzBj5cp2vg&s)

## Improve Your Resume with ATS

Smart ATS is an innovative Applicant Tracking System (ATS) designed to help job seekers improve their resumes by analyzing them against job descriptions. The system provides professional evaluation, percentage match, and improvisation suggestions, leveraging Google's Generative AI.

## Features

- **Resume Analysis**: Professional evaluation of resumes against job descriptions.
- **Percentage Match**: Calculates the percentage match of the resume with the job description.
- **Improvisation Suggestions**: Provides suggestions for improving the resume based on the analysis.
- **PDF Viewer**: Displays the uploaded PDF resume within the application.
- **Downloadable Reports**: Users can download analysis reports and suggestions.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8+
- Pip

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Garry864/Smart-ATS-Advisor.git
    cd smart-ats
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add your Google API key:

    ```env
    API=your-google-api-key
    ```

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
