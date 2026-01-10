import streamlit as st
import PyPDF2

st.set_page_config(page_title="Intelligent Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.caption("Role-Based AI Resume Screening")

# ---------------- ROLE SELECTION ----------------
role = st.sidebar.radio("Select Your Role", ["Candidate", "Recruiter"])

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ---------------- CANDIDATE SCREEN ----------------
if role == "Candidate":
    st.header("👤 Candidate Resume Screening")

    resume_file = st.file_uploader("📤 Upload Your Resume (PDF)", type=["pdf"])
    skills = st.text_input("💡 Skills (comma separated)")
    education = st.text_input("🎓 Education")
    experience = st.slider("🧑‍💻 Years of Experience", 0, 10, 0)

    if resume_file:
        resume_text = read_pdf(resume_file)
        combined_text = resume_text + " " + skills + " " + education

        
        

        result = analyze_resume(combined_text, jd_text)

        st.markdown("---")
        st.subheader("📊 Resume Evaluation Feedback")

        st.metric("Resume Strength Score", f"{result['score']}%")
        st.progress(result["score"] / 100)

        st.subheader("✅ Skills Identified")
        for skill in result["matched_skills"]:
            st.write("•", skill)

        st.subheader("⚠️ Skills to Improve")
        for skill in result["missing_skills"]:
            st.write("•", skill)

        st.info("💡 Tip: Add missing skills or certifications to improve your resume")

# ---------------- RECRUITER SCREEN ----------------
if role == "Recruiter":
    st.header("🧑‍💼 Recruiter Resume Screening")

    jd_text = st.text_area(
        "📄 Paste Job Description",
        height=200,
        
    )

    resume_file = st.file_uploader("📤 Upload Candidate Resume (PDF)", type=["pdf"])

    candidate_name = st.text_input("Candidate Name")
    experience = st.slider("Years of Experience", 0, 15, 1)

    if resume_file and jd_text:
        resume_text = read_pdf(resume_file)
        result = analyze_resume(resume_text, jd_text)

        st.markdown("---")
        st.subheader("📊 Screening Results")

        st.metric("Match Score", f"{result['score']}%")
        st.progress(result["score"] / 100)

        if result["recommendation"] == "SHORTLIST":
            st.success("✅ AI Recommendation: SHORTLIST")
        else:
            st.error("❌ AI Recommendation: REJECT")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✔ Matched Skills")
            for skill in result["matched_skills"]:
                st.write("•", skill)

        with col2:
            st.subheader("❌ Missing Skills")
            for skill in result["missing_skills"]:
                st.write("•", skill)

        st.markdown("---")
        st.subheader("📄 Candidate Summary")
        st.write(f"**Name:** {candidate_name}")
        st.write(f"**Experience:** {experience} years")

    st.markdown("---")
    st.subheader("🎓 Profile Summary")
    st.write(f"**Education:** {education}")
    st.write(f"**Experience:** {experience} years")

