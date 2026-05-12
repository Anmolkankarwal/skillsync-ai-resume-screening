from flask import Flask, render_template, request
from resume_parser import read_pdf, read_docx, clean_text
from matcher import calculate_match

app = Flask(__name__)

# ===================================
# HOME PAGE
# ===================================

@app.route("/")
def index():

    return render_template("index.html")


# ===================================
# MATCH ROUTE
# ===================================

@app.route("/match", methods=["POST"])
def match():

    # -------------------------
    # GET FORM DATA
    # -------------------------

    resume = request.files["resume"]

    job_desc = request.form["job_description"]

    # -------------------------
    # VALIDATION
    # -------------------------

    if resume.filename == "":

        return render_template(
            "index.html",
            error="Please upload a resume file."
        )

    # -------------------------
    # READ RESUME
    # -------------------------

    if resume.filename.endswith(".pdf"):

        resume_text = read_pdf(resume)

    elif resume.filename.endswith(".docx"):

        resume_text = read_docx(resume)

    else:

        return render_template(
            "index.html",
            error="Only PDF and DOCX files are supported."
        )

    # -------------------------
    # CLEAN TEXT
    # -------------------------

    resume_text = clean_text(resume_text)

    job_desc = clean_text(job_desc)

    # -------------------------
    # MATCH ENGINE
    # -------------------------

    result = calculate_match(
        resume_text,
        job_desc
    )

    # -------------------------
    # EXTRACT RESULTS
    # -------------------------

    score = result["final_score"]

    matched_skills = result["matched_skills"]

    missing_skills = result["missing_skills"]

    recommendation = result["recommendation"]

    keyword_score = result["keyword_score"]

    skills_score = result["skills_score"]

    experience_score = result["experience_score"]

    # -------------------------
    # MATCH CATEGORY
    # -------------------------

    if score >= 85:

        category = "Great Match"

    elif score >= 70:

        category = "Good Match"

    elif score >= 40:

        category = "Average Match"

    else:

        category = "Poor Match"

    # -------------------------
    # RENDER TEMPLATE
    # -------------------------

    return render_template(

        "index.html",

        score=score,

        category=category,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        recommendation=recommendation,

        keyword_score=keyword_score,

        skills_score=skills_score,

        experience_score=experience_score
    )


# ===================================
# RUN APP
# ===================================

if __name__ == "__main__":

    app.run(debug=True)