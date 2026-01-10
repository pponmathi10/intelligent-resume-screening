import streamlit as st
import PyPDF2
from model import analyze_resume

st.set_page_config(page_title="Intelligent Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.caption("AI-powered resume screening for candidates and recruiters")

# --------- Utility ---------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# --------- Role Selection ---------
role = st.sidebar.radio("Select Role", ["Candidate", "Recruiter"])

# ================== CANDIDATE SCREEN ==================
if role == "Candidate":
    st.header("👤 Candidate Resume Screening")

    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    skills = st.text_input("Skills (comma separated)")
    education = st.text_input("Education")
    experience = st.slider("Years of Experience", 0, 15, 0)

    if resume_file:
        resume_text = read_pdf(resume_file)
        combined_resume = resume_text + " " + skills + " " + education

        with open("sample_jd.txt") as f:
            jd_text = f.read()

        result = analyze_resume(combined_resume, jd_text)

        st.markdown("---")
        st.subheader("📊 Resume Feedback")

        st.metric("Resume Strength Score", f"{result['score']}%")
        st.progress(result["score"] / 100)

        st.subheader("✅ Matched Skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.write("•", skill)
        else:
            st.write("No matched skills found")

        st.subheader("⚠ Skills to Improve")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.write("•", skill)
        else:
            st.write("No missing skills")

        st.info("💡 Improve your resume by adding missing skills and certifications.")

# ================== RECRUITER SCREEN ==================
if role == "Recruiter":
    st.header("🧑‍💼 Recruiter Resume Screening")

    with open("sample_jd.txt") as f:
        default_jd = f.read()

    jd_text = st.text_area("Paste Job Description", height=200, value=default_jd)

    resume_file = st.file_uploader("Upload Candidate Resume (PDF)", type=["pdf"])
    candidate_name = st.text_input("Candidate Name")
    experience = st.slider("Candidate Experience (Years)", 0, 20, 1)

    if resume_file and jd_text.strip() != "":
        resume_text = read_pdf(resume_file)
        result = analyze_resume(resume_text, jd_text)

        st.markdown("---")
        st.subheader("📊 Screening Result")

        st.metric("Match Score", f"{result['score']}%")
        st.progress(result["score"] / 100)

        if result["recommendation"] == "SHORTLIST":
            st.success("✅ AI Recommendation: SHORTLIST")
        else:
            st.error("❌ AI Recommendation: REJECT")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✔ Matched Skills")
            if result["matched_skills"]:
                for skill in result["matched_skills"]:
                    st.write("•", skill)
            else:
                st.write("None")

        with col2:
            st.subheader("❌ Missing Skills")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.write("•", skill)
            else:
                st.write("None")

        st.markdown("---")
        st.subheader("📄 Candidate Summary")
        st.write(f"**Name:** {candidate_name}")
        st.write(f"**Experience:** {experience} years")

