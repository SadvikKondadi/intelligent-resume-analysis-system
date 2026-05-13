import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resumeFile) {
      alert("Please upload resume.");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please paste job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);
      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
    } catch (error) {
      alert("Error analyzing resume. Please check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <section className="hero">
        <div className="heroText">
          <span className="badge">Intelligent Resume Analysis System</span>
          <h1>Smart ATS Resume Analyzer</h1>
          <p>
            Upload your resume, paste any job description, and get instant match
            score, missing skills, keywords, and improvement suggestions.
          </p>
        </div>

        <div className="glassCard">
          <div className="uploadBox">
            <label>Upload Resume</label>
            <p>Supported formats: PDF, DOCX, TXT</p>
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={(e) => setResumeFile(e.target.files[0])}
            />
            {resumeFile && <h4>Selected: {resumeFile.name}</h4>}
          </div>

          <textarea
            className="jdBox"
            placeholder="Paste job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <button onClick={analyzeResume} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </div>
      </section>

      {result && (
        <section className="resultSection">
          <div className="scoreCard">
            <h2>{result.score}%</h2>
            <p>Final ATS Match Score</p>
          </div>

          <div className="grid">
            <div className="card">
              <h3>Resume Similarity</h3>
              <p className="metric">{result.similarity_score}%</p>
            </div>

            <div className="card">
              <h3>Skill Match</h3>
              <p className="metric">{result.skill_score}%</p>
            </div>

            <div className="card wide">
              <h3>Overall Feedback</h3>
              <p>{result.feedback}</p>
            </div>

            <div className="card">
              <h3>Matched Skills</h3>
              <ul>
                {result.matched.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="card">
              <h3>Missing Skills</h3>
              <ul>
                {result.missing.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="card wide">
              <h3>Suggestions</h3>
              <ul>
                {result.suggestions.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      )}

      <footer>
        <p>Developed by <strong>Sadvik Kondadi</strong></p>
      </footer>
    </div>
  );
}

export default App;