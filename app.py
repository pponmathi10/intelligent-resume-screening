import streamlit as st
import PyPDF2


st.set_page_config(page_title="Intelligent Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.subheader("AI-Powered Resume Evaluation")

# Job Description
st.sidebar.header("📄 Job Description")
jd_text = st.sidebar.text_area(
    "Paste Job Description",
    height=250,
    value=open("sample_jd.txt").read()
)

# Resume Upload
st.header("📤 Upload Resume (PDF)")
resume_file = st.file_uploader("Upload Resume", type=["pdf"])

# Manual Details
st.header("📝 Candidate Details")
skills = st.text_input("Skills (comma separated)")
education = st.text_input("Education")
experience = st.slider("Years of Experience", 0, 10, 1)

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if resume_file:
    resume_text = read_pdf(resume_file)
    combined_resume = resume_text + " " + skills + " " + education

    result = analyze_resume(combined_resume, jd_text)

    st.markdown("---")
    st.header("📊 Screening Results")

    # Match Score
    st.metric("Overall Match Score", f"{result['score']}%")
    st.progress(result["score"] / 100)

    # Recommendation
    if result["recommendation"] == "SHORTLIST":
        st.success("✅ AI Recommendation: SHORTLIST")
    else:
        st.error("❌ AI Recommendation: REJECT")

    # Skill Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✔ Matched Skills")
        for skill in result["matched_skills"]:
            st.write("•", skill)

    with col2:
        st.subheader("❌ Missing Skills")
        for skill in result["missing_skills"]:
            st.write("•", skill)

    # Experience & Education
    st.markdown("---")
    st.subheader("🎓 Profile Summary")
    st.write(f"**Education:** {education}")
    st.write(f"**Experience:** {experience} years")

