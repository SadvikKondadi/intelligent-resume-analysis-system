import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

common_words = {
    "the", "and", "or", "to", "of", "in", "for", "with", "on",
    "a", "an", "is", "are", "as", "by", "be", "this", "that",
    "from", "at", "will", "you", "your", "we", "our", "job",
    "role", "team", "work", "experience", "while", "including",
    "status", "services", "service", "customer", "customers",
    "technology", "technologies", "environment", "using",
    "used", "application", "applications", "development",
    "developer", "software", "systems", "system", "build",
    "building", "based", "their", "these", "those", "through",
    "into", "about", "such", "have", "has", "had", "been",
    "more", "than", "other", "can", "also", "all"
}

important_skills = [
    "python", "java", "javascript", "react", "node", "flask", "sql",
    "mongodb", "postgresql", "mysql", "git", "github", "linux",
    "data structures", "algorithms", "oop", "rest api", "api",
    "machine learning", "nlp", "aws", "cloud", "docker", "kubernetes",
    "ci cd", "debugging", "distributed systems", "microservices",
    "database", "backend", "frontend", "full stack"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text, top_n=25):
    text = clean_text(text)
    words = text.split()

    keywords = []

    for word in words:
        if len(word) > 2 and word not in common_words:
            keywords.append(word)

    freq = {}

    for word in keywords:
        freq[word] = freq.get(word, 0) + 1

    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    return [word for word, count in sorted_keywords[:top_n]]

def find_skill_matches(resume_text, job_description):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    matched_skills = []
    missing_skills = []

    for skill in important_skills:
        if skill in jd_clean:
            if skill in resume_clean:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    return matched_skills, missing_skills

def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(similarity * 100, 2)

def analyze_resume(resume, job_description):
    resume_clean = clean_text(resume)
    jd_clean = clean_text(job_description)

    matched_skills, missing_skills = find_skill_matches(resume_clean, jd_clean)

    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume)

    missing_keywords = []

    for keyword in jd_keywords:
        if keyword not in resume_clean:
            missing_keywords.append(keyword)

    similarity_score = calculate_similarity(resume, job_description)

    skill_score = int(
        (len(matched_skills) / max(len(matched_skills) + len(missing_skills), 1)) * 100
    )

    final_score = int((similarity_score * 0.6) + (skill_score * 0.4))

    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Add project or experience related to {skill}")

    for keyword in missing_keywords[:8]:
        suggestions.append(f"Include keyword if truthful: {keyword}")

    if final_score >= 80:
        overall_feedback = "Strong match for this job description."
    elif final_score >= 60:
        overall_feedback = "Moderate match. Improve missing skills and keywords."
    else:
        overall_feedback = "Low match. Resume needs stronger alignment with this job description."

    return {
        "score": final_score,
        "similarity_score": similarity_score,
        "skill_score": skill_score,
        "matched": matched_skills,
        "missing": missing_skills,
        "missing_keywords": missing_keywords[:15],
        "suggestions": suggestions[:15],
        "feedback": overall_feedback
    }