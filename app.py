import streamlit as st
import pandas as pd




# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Resume Screening System", layout="centered")
st.title("📄 Intelligent Resume Screening System")
st.subheader("Using NLP and Machine Learning")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("AI_Resume_Screening.csv")

# Combine dataset text columns
df["resume_text"] = (
    df["Skills"].fillna("") + " " +
    df["Education"].fillna("") + " " +
    df["Certifications"].fillna("") + " " +
    df["Job Role"].fillna("") + " " +
    df["Experience (Years)"].astype(str)
)

X = df["resume_text"]
y = df["Recruiter Decision"]

# ---------------- TRAIN MODEL ----------------






# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(uploaded_file):
   
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ---------------- USER INPUT SECTION ----------------
st.markdown("## 🧑 Candidate Details")

skills = st.text_input("Skills (comma separated)")
education = st.selectbox(
    "Education",
    ["B.E","B.Sc", "B.Tech", "M.Sc", "MBA", "PhD"]
)
certifications = st.text_input("Certifications")
experience = st.slider("Experience (Years)", 0, 20, 1)

job_role = st.text_input("Job Role Applied For")

st.markdown("## 📤 Upload Resume")
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or TXT)",
    type=["pdf", "txt"]
)

manual_resume = st.text_area(
    "OR paste resume text (optional)",
    height=150
)

# ---------------- PREDICTION ----------------
if st.button("🚀 Screen My Resume"):

    resume_text = ""

    # Priority: uploaded resume
   

    # Combine resume + form details
    final_text = (
        resume_text + " " +
        skills + " " +
        education + " " +
        certifications + " " +
        job_role + " " +
        str(experience)
    )

    


