
"use client";

import { useState } from "react";

type InterviewConfig = {
  role: string;
  type: string;
  difficulty: string;
  questionCount: string;
  duration: string;
};

type QuestionResponse = {
  role: string;
  difficulty: string;
  total_questions: number;
  questions: string[];
};

export default function InterviewSetup() {
  const [role, setRole] = useState("Python Developer");
  const [type, setType] = useState("Technical");
  const [difficulty, setDifficulty] = useState("medium");
  const [questionCount, setQuestionCount] = useState("3");
  const [duration, setDuration] = useState("30");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleStart() {
    setLoading(true);
    setError("");

    const config: InterviewConfig = {
      role,
      type,
      difficulty,
      questionCount,
      duration,
    };

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/questions/?role=${encodeURIComponent(config.role)}&difficulty=${encodeURIComponent(config.difficulty)}`
      );

      if (!response.ok) {
        throw new Error(`Backend returned error: ${response.status}`);
      }

      const data: QuestionResponse = await response.json();

      sessionStorage.setItem(
        "interviewQuestions",
        JSON.stringify(data)
      );

      sessionStorage.setItem(
        "interviewConfig",
        JSON.stringify(config)
      );

      window.location.href = "/interview/session";

    } catch (err) {
      console.error("Interview API error:", err);

      setError(
        "Unable to connect to the interview server. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="interview-page">
      <header className="interview-header">
        <a href="/" className="back-link">← Back to Dashboard</a>
        <span className="setup-status"><i /> AI INTERVIEW SETUP</span>
      </header>

      <section className="interview-intro">
        <div className="eyebrow">YOUR NEXT CAREER MOVE STARTS HERE</div>
        <h1>Design your <span>interview.</span></h1>
        <p>Customize your practice session and let your AI interviewer take it from there.</p>
      </section>

      <div className="interview-layout">
        <section className="setup-panel">
          <div className="setup-title">
            <div>
              <h2>Interview Configuration</h2>
              <p>Choose the settings for your practice session.</p>
            </div>
            <div className="settings-icon">⚙</div>
          </div>

          <div className="field-group">
            <label htmlFor="role">TARGET JOB ROLE</label>
            <select id="role" value={role} onChange={(e) => setRole(e.target.value)}>
              <option>Python Developer</option>
              <option>Machine Learning Engineer</option>
              <option>Data Scientist</option>
              <option>Data Analyst</option>
              <option>Frontend Developer</option>
              <option>Backend Developer</option>
              <option>Full Stack Developer</option>
            </select>
          </div>

          <div className="field-group">
            <label>INTERVIEW TYPE</label>
            <div className="choice-grid">
              {["Technical", "HR", "Mixed"].map((item) => (
                <button
                  key={item}
                  className={`choice-card ${type === item ? "selected" : ""}`}
                  onClick={() => setType(item)}
                  type="button"
                >
                  <span>{item === "Technical" ? "⌘" : item === "HR" ? "♙" : "◈"}</span>
                  <strong>{item}</strong>
                  <small>{item === "Technical" ? "Technical skills" : item === "HR" ? "Behavioral questions" : "Both formats"}</small>
                </button>
              ))}
            </div>
          </div>

          <div className="field-group">
            <label>DIFFICULTY LEVEL</label>
            <div className="difficulty-grid">
              {["Easy", "Medium", "Hard"].map((item) => (
                <button
                  key={item}
                  type="button"
                  className={`difficulty-option ${difficulty === item.toLowerCase() ? "selected" : ""}`}
                  onClick={() => setDifficulty(item.toLowerCase())}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          <div className="form-divider" />

          <div className="field-grid">
            <div className="field-group">
              <label htmlFor="questions">NUMBER OF QUESTIONS</label>
              <select id="questions" value={questionCount} onChange={(e) => setQuestionCount(e.target.value)}>
                <option value="3">3 Questions</option>
                <option value="5">5 Questions</option>
                <option value="10">10 Questions</option>
                <option value="15">15 Questions</option>
              </select>
            </div>

            <div className="field-group">
              <label htmlFor="duration">DURATION</label>
              <select id="duration" value={duration} onChange={(e) => setDuration(e.target.value)}>
                <option value="15">15 Minutes</option>
                <option value="30">30 Minutes</option>
                <option value="45">45 Minutes</option>
                <option value="60">60 Minutes</option>
              </select>
            </div>
          </div>

          {error && <p className="error-message">{error}</p>}

          <button
            className="start-interview-button"
            onClick={handleStart}
            disabled={loading}
          >
            {loading ? "Preparing your interview..." : "Start Interview"}
            <span>{loading ? "..." : "→"}</span>
          </button>

          <p className="privacy-note">
            ✦ Your practice session is designed around your selected preferences.
          </p>
        </section>

        <aside className="interview-sidebar">
          <div className="preview-card">
            <div className="preview-label">SESSION PREVIEW</div>
            <div className="preview-art">AI</div>
            <h3>{role}</h3>
            <p>Your personalized interview session</p>
            <div className="preview-divider" />
            <div className="preview-detail"><span>Interview type</span><strong>{type}</strong></div>
            <div className="preview-detail"><span>Difficulty</span><strong>{difficulty}</strong></div>
            <div className="preview-detail"><span>Questions</span><strong>{questionCount}</strong></div>
            <div className="preview-detail"><span>Duration</span><strong>{duration} min</strong></div>
          </div>

          <div className="tip-card">
            <div className="tip-icon">✦</div>
            <strong>Pro preparation tip</strong>
            <p>Answer with specific examples. Explain your thought process, not just the final result.</p>
          </div>
        </aside>
      </div>
    </main>
  );
}
