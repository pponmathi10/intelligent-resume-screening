import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    skills = [
        "python", "java", "machine learning", "deep learning",
        "sql", "html", "css", "javascript",
        "data science", "nlp", "aws", "docker"
    ]
    text = text.lower()
    return [skill for skill in skills if skill in text]

def match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def analyze_resume(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = match_score(resume_text, jd_text)

    recommendation = "SHORTLIST" if score >= 70 else "REJECT"

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendation": recommendation
    }
