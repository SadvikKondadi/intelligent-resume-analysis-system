from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_analyzer import analyze_resume
import PyPDF2
import docx

app = Flask(__name__)
CORS(app)

def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def extract_docx_text(file):
    document = docx.Document(file)
    text = ""

    for para in document.paragraphs:
        text += para.text + "\n"

    return text

@app.route("/analyze", methods=["POST"])
def analyze():
    job_description = request.form.get("job_description", "")
    resume_text = ""

    if "resume_file" in request.files:
        file = request.files["resume_file"]
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            resume_text = extract_pdf_text(file)

        elif filename.endswith(".docx"):
            resume_text = extract_docx_text(file)

        elif filename.endswith(".txt"):
            resume_text = file.read().decode("utf-8")

        else:
            return jsonify({
                "error": "Only PDF, DOCX, and TXT supported"
            }), 400

    result = analyze_resume(resume_text, job_description)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)