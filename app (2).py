import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import io
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Recruiter Pro", page_icon="👔", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_stdio=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return None

# --- UI HEADER ---
st.title("👔 Intelligent Resume Screening System")
st.markdown("🚀 **Recruiter Dashboard:** Instantly rank candidates based on semantic match with your Job Description.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area("Paste the Job Description (JD) here:", height=300, 
                            placeholder="Example: Looking for a Data Scientist with Python, SQL, and NLP experience...")

with col2:
    st.subheader("📂 Candidate Resumes")
    uploaded_files = st.file_uploader("Upload Resumes (PDF format only)", type=["pdf"], accept_multiple_files=True)

# --- ANALYSIS LOGIC ---
if st.button("Analyze & Rank Candidates"):
    if not jd_input:
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Our AI is evaluating candidates..."):
            # 1. Process JD
            cleaned_jd = clean_text(jd_input)
            
            # 2. Process Resumes
            resume_names = []
            resume_texts = []
            
            for file in uploaded_files:
                raw_text = extract_text_from_pdf(file)
                if raw_text:
                    resume_texts.append(clean_text(raw_text))
                    resume_names.append(file.name)
            
            if resume_texts:
                # 3. ML Pipeline: TF-IDF with Bigrams
                vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
                all_content = [cleaned_jd] + resume_texts
                tfidf_matrix = vectorizer.fit_transform(all_content)
                
                # 4. Similarity Calculation
                # Compare JD (index 0) against all Resumes (index 1 onwards)
                scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
                
                # 5. Result Formatting
                results_df = pd.DataFrame({
                    "Candidate Name": resume_names,
                    "Match Score (%)": [round(s * 100, 2) for s in scores]
                }).sort_values(by="Match Score (%)", ascending=False)
                
                # --- OUTPUT DASHBOARD ---
                st.success(f"Analysis complete! Processed {len(resume_names)} resumes.")
                
                # Top Metrics
                m1, m2 = st.columns(2)
                m1.metric("Highest Match", f"{results_df.iloc[0]['Match Score (%)']}%")
                m2.metric("Average Match", f"{round(results_df['Match Score (%)'].mean(), 2)}%")
                
                # Visual Chart
                st.subheader("📊 Ranking Visualization")
                fig = px.bar(results_df, x="Match Score (%)", y="Candidate Name", 
                             orientation='h', color='Match Score (%)',
                             color_continuous_scale='Greens', text='Match Score (%)')
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Data Table
                st.subheader("📋 Detailed Results")
                st.dataframe(results_df, use_container_width=True)
                
                # Download CSV
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Ranking Report", data=csv, 
                                   file_name="resume_ranking.csv", mime="text/csv")
            else:
                st.error("Could not extract text from the uploaded PDFs. Please check if they are scanned images.")

# --- UI HEADER ---
st.title("👔 Intelligent Resume Screening System")
st.markdown("🚀 **Recruiter Dashboard:** Instantly rank candidates based on semantic match with your Job Description.")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area("Paste the Job Description (JD) here:", height=300, 
                            placeholder="Example: Looking for a Data Scientist with Python, SQL, and NLP experience...")

with col2:
    st.subheader("📂 Candidate Resumes")
    uploaded_files = st.file_uploader("Upload Resumes (PDF format only)", type=["pdf"], accept_multiple_files=True)

# --- ANALYSIS LOGIC ---
if st.button("Analyze & Rank Candidates"):
    if not jd_input:
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Our AI is evaluating candidates..."):
            # 1. Process JD
            cleaned_jd = clean_text(jd_input)
            
            # 2. Process Resumes
            resume_names = []
            resume_texts = []
            
            for file in uploaded_files:
                raw_text = extract_text_from_pdf(file)
                if raw_text:
                    resume_texts.append(clean_text(raw_text))
                    resume_names.append(file.name)
            
            if resume_texts:
                # 3. ML Pipeline: TF-IDF with Bigrams
                vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
                all_content = [cleaned_jd] + resume_texts
                tfidf_matrix = vectorizer.fit_transform(all_content)
                
                # 4. Similarity Calculation
                # Compare JD (index 0) against all Resumes (index 1 onwards)
                scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
                
                # 5. Result Formatting
                results_df = pd.DataFrame({
                    "Candidate Name": resume_names,
                    "Match Score (%)": [round(s * 100, 2) for s in scores]
                }).sort_values(by="Match Score (%)", ascending=False)
                
                # --- OUTPUT DASHBOARD ---
                st.success(f"Analysis complete! Processed {len(resume_names)} resumes.")
                
                # Top Metrics
                m1, m2 = st.columns(2)
                m1.metric("Highest Match", f"{results_df.iloc[0]['Match Score (%)']}%")
                m2.metric("Average Match", f"{round(results_df['Match Score (%)'].mean(), 2)}%")
                
                # Visual Chart
                st.subheader("📊 Ranking Visualization")
                fig = px.bar(results_df, x="Match Score (%)", y="Candidate Name", 
                             orientation='h', color='Match Score (%)',
                             color_continuous_scale='Greens', text='Match Score (%)')
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Data Table
                st.subheader("📋 Detailed Results")
                st.dataframe(results_df, use_container_width=True)
                
                # Download CSV
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Ranking Report", data=csv, 
                                   file_name="resume_ranking.csv", mime="text/csv")
            else:
                st.error("Could not extract text from the uploaded PDFs. Please check if they are scanned images.")

