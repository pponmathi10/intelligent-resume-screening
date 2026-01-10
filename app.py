import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import io

# Page Config
st.set_page_config(page_title="AI Resume Intelligence", page_icon="🎯", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stProgress > div > div > div > div { background-color: #007bff; }
    </style>
    """, unsafe_allow_stdio=True)

def extract_text(file):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip()
    except:
        return ""

# Sidebar
st.sidebar.title("Settings")
st.sidebar.info("This system uses TF-IDF Vectorization and Cosine Similarity to rank candidates.")

# Main UI
st.title("🤖 Intelligent Resume Screening Dashboard")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Job Description")
    jd = st.text_area("Paste the target Job Description here...", height=250, placeholder="Required skills: Python, SQL, Machine Learning...")

with col2:
    st.subheader("📤 Candidate Resumes")
    uploaded_files = st.file_uploader("Upload multiple PDF resumes", type="pdf", accept_multiple_files=True)

if st.button("🚀 Run Intelligence Analysis"):
    if jd and uploaded_files:
        with st.spinner("Processing NLP Models..."):
            # Extraction
            data = []
            for file in uploaded_files:
                content = extract_text(file)
                if content:
                    data.append({"filename": file.name, "text": content})
            
            if data:
                # ML Engine
                texts = [jd] + [d['text'] for d in data]
                vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
                tfidf_matrix = vectorizer.fit_transform(texts)
                
                # Calculation
                scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
                
                # Results DataFrame
                df = pd.DataFrame({
                    "Candidate": [d['filename'] for d in data],
                    "Score": [round(s * 100, 2) for s in scores]
                }).sort_values(by="Score", ascending=False)

                st.markdown("---")
                
                # Metrics
                top_col1, top_col2 = st.columns(2)
                top_col1.metric("Top Score", f"{df.iloc[0]['Score']}%")
                top_col2.metric("Candidates Processed", len(df))

                # Visuals
                fig = px.bar(df, x="Score", y="Candidate", orientation='h', 
                             title="Candidate Match Ranking",
                             color="Score", color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

                # Detailed Table
                st.subheader("Detailed Ranking")
                st.dataframe(df, use_container_width=True)
                
                # Download CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report (CSV)", csv, "screening_report.csv", "text/csv")
            else:
                st.error("Could not extract text. Ensure PDFs are not scanned images.")
    else:
        st.warning("Please provide both a Job Description and at least one Resume.")


