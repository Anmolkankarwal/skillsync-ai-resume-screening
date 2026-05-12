from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===================================
# SKILLS DATABASE
# ===================================

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "node",
    "mongodb",
    "sql",
    "mysql",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "docker",
    "aws",
    "html",
    "css",
    "firebase"

]

# ===================================
# EXTRACT SKILLS
# ===================================

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:

            found_skills.append(skill)

    return list(set(found_skills))

# ===================================
# MAIN FUNCTION
# ===================================

def calculate_match(resume_text, job_desc):

    documents = [resume_text, job_desc]

    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    similarity_score = round(similarity * 100, 2)

    # SKILLS

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_desc)

    matched_skills = list(
        set(resume_skills).intersection(set(jd_skills))
    )

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    # FINAL SCORE

    if len(jd_skills) > 0:

        skill_score = (
            len(matched_skills) / len(jd_skills)
        ) * 100

    else:

        skill_score = 0

    final_score = (
        similarity_score * 0.7
        +
        skill_score * 0.3
    )

    final_score = round(final_score, 2)

    # RECOMMENDATION

    if final_score >= 80:

        recommendation = (
            "Candidate strongly matches the role."
        )

    elif final_score >= 60:

        recommendation = (
            "Candidate partially matches the role."
        )

    else:

        recommendation = (
            "Candidate lacks important required skills."
        )

    # SUGGESTIONS

    suggestions = []

    if len(missing_skills) > 0:

        suggestions.append(
            "Add missing skills from the job description."
        )

    if similarity_score < 60:

        suggestions.append(
            "Improve ATS keyword optimization."
        )

    return {

        "final_score": final_score,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "recommendation": recommendation,

        "keyword_score": round(similarity_score),

        "skills_score": round(skill_score),

        "experience_score": round(final_score + 10),

        "suggestions": suggestions
    }