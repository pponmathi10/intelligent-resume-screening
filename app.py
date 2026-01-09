import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Resume Screening System", layout="centered")
st.title("📄 Intelligent Resume Screening System")
st.subheader("Using NLP and Machine Learning")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("AI_Resume_Screening.csv")

# Combine text columns for training
df["resume_text"] = (
    df["Skills"].fillna("") + " " +
    df["Education"].fillna("") + " " +
    df["Certifications"].fillna("") + " " +
    df["Job Role"].fillna("")
)

X = df["resume_text"]
y = df["Recruiter Decision"]

# ---------------- TRAIN MODEL ----------------
vectorizer = TfidfVectorizer(stop_words="english", max_features=4000)
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ---------------- RESUME UPLOAD ----------------
st.markdown("### 📤 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or TXT)",
    type=["pdf", "txt"]
)

manual_text = st.text_area(
    "OR paste resume text here",
    height=200
)

# ---------------- PREDICTION ----------------
if st.button("🚀 Screen Resume"):

    resume_text = ""

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = uploaded_file.read().decode("utf-8")

    elif manual_text.strip() != "":
        resume_text = manual_text

    else:
        st.warning("Please upload a resume or paste text.")
        st.stop()

    resume_vec = vectorizer.transform([resume_text])
    prediction = model.predict(resume_vec)[0]
    confidence = max(model.predict_proba(resume_vec)[0]) * 100

    st.markdown(f"## ✅ Recruiter Decision: **{prediction}**")
    st.markdown(f"### 📊 Confidence Score: **{confidence:.2f}%**")

    if prediction == "Hire":
        st.success("Candidate is suitable for the job 🎯")
    else:
        st.error("Candidate does not meet the requirements ❌")
