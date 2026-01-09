import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.title("Intelligent Resume Screening System")

# Load dataset
df = pd.read_csv("AI_Resume_Screening.csv")

# Combine text columns
df["text"] = (
    df["Skills"].fillna("") + " " +
    df["Education"].fillna("") + " " +
    df["Certifications"].fillna("") + " " +
    df["Job Role"].fillna("")
)

X = df["text"]
y = df["Recruiter Decision"]

# Train model
vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# User input
skills = st.text_input("Enter Skills")
education = st.text_input("Enter Education")
certifications = st.text_input("Enter Certifications")
job_role = st.text_input("Enter Job Role")

if st.button("Screen Resume"):
    resume_text = skills + " " + education + " " + certifications + " " + job_role
    resume_vec = vectorizer.transform([resume_text])
    prediction = model.predict(resume_vec)[0]

    st.success(f"Recruiter Decision: {prediction}")
