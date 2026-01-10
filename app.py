import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Intelligent Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.caption("AI-powered resume screening for Candidates & Recruiters")

# ---------------- SKILLS DATABASE ----------------
SKILLS = [
    "python", "java", "machine learning", "data science",
    "sql", "html", "css", "javascript",
    "aws", "docker", "nlp", "deep learning"
]

# ---------------- FUNCTIONS ----------------
def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS if skill in text]

def calculate_score(resume, jd):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, jd])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

# ---------------- ROLE SELECTION ----------------
role = st.sidebar.radio("Select Role", ["Candidate", "Recruiter"])

# ================== CANDIDATE SCREEN ==================
if role == "Candidate":
    st.header("👤 Candidate Resume Screening")

    resume_text = st.text_area(
        "📄 Paste Your Resume Text",
        height=250,
        placeholder="Paste your resume content here..."
    )

    skills_input = st.text_input("💡 Skills (comma separated)")
    education = st.text_input("🎓 Education")
    experience = st.slider("🧑‍💻 Years of Experience", 0, 20, 0)

    if resume_text.strip() != "":
        jd_sample = """
        Software Developer with skills in Python, Java, SQL,
        Machine Learning and experience in real-world projects.
        """

        full_resume = resume_text + " " + skills_input + " " + education

        score = calculate_score(full_resume, jd_sample)
        matched = extract_skills(full_resume)
        missing = list(set(SKILLS) - set(matched))

        st.markdown("---")
        st.subheader("📊 Resume Evaluation Result")

        st.metric("Resume Strength Score", f"{score}%")
        st.progress(score / 100)

        st.subheader("✅ Skills Detected")
        for s in matched:
            st.write("•", s)

        st.subheader("⚠ Skills to Improve")
        for s in missing[:5]:
            st.write("•", s)

        st.info("💡 Tip: Add missing technical skills and project experience.")

# ================== RECRUITER SCREEN ==================
if role == "Recruiter":
    st.header("🧑‍💼 Recruiter Resume Screening")

    jd_text = st.text_area(
        "📄 Paste Job Description",
        height=200,
        placeholder="Paste job description here..."
    )

    resume_text = st.text_area(
        "📄 Paste Candidate Resume",
        height=200,
        placeholder="Paste candidate resume here..."
    )

    candidate_name = st.text_input("Candidate Name")
    experience = st.slider("Candidate Experience (Years)", 0, 20, 1)

    if resume_text.strip() != "" and jd_text.strip() != "":
        score = calculate_score(resume_text, jd_text)
        matched = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        missing = list(set(jd_skills) - set(matched))

        recommendation = "SHORTLIST" if score >= 70 else "REJECT"

        st.markdown("---")
        st.subheader("📊 Screening Result")

        st.metric("Match Score", f"{score}%")
        st.progress(score / 100)

        if recommendation == "SHORTLIST":
            st.success("✅ AI Recommendation: SHORTLIST")
        else:
            st.error("❌ AI Recommendation: REJECT")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✔ Matched Skills")
            for s in matched:
                st.write("•", s)

        with col2:
            st.subheader("❌ Missing Skills")
            for s in missing:
                st.write("•", s)

        st.markdown("---")
        st.subheader("📄 Candidate Summary")
        st.write(f"**Name:** {candidate_name}")
        st.write(f"**Experience:** {experience} years")
       

        st.markdown("---")
        st.subheader("📊 Resume Feedback")

      
        

        
        
          
               
       
       
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

