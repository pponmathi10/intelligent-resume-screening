from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python", "java", "machine learning", "deep learning",
    "sql", "html", "css", "javascript",
    "data science", "nlp", "aws", "docker"
]

def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS if skill in text]

def calculate_match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def analyze_resume(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = calculate_match_score(resume_text, jd_text)
    recommendation = "SHORTLIST" if score >= 70 else "REJECT"

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendation": recommendation
    }

