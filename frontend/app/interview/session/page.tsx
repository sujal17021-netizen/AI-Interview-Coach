
"use client";

import { useEffect, useState } from "react";

type InterviewData = {
  role: string;
  difficulty: string;
  total_questions: number;
  questions: string[];
};

type EvaluationResult = {
  question: string;
  predicted_score: number;
  maximum_score: number;
  evaluation_type: string;
};

export default function InterviewSession() {
  const [interview, setInterview] = useState<InterviewData | null>(null);
  const [candidateName, setCandidateName] = useState("");
  const [answer, setAnswer] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [completed, setCompleted] = useState(false);
  const [evaluationResults, setEvaluationResults] =
    useState<EvaluationResult[]>([]);

  useEffect(() => {
    const saved = sessionStorage.getItem("interviewQuestions");

    if (saved) {
      try {
        setInterview(JSON.parse(saved));
      } catch {
        setMessage("Invalid interview data. Please start a new interview.");
      }
    } else {
      setMessage("No interview found. Please configure a new interview.");
    }

    setLoading(false);
  }, []);

  async function submitAnswer() {
    if (!interview) return;

    if (candidateName.trim().length < 2) {
      setMessage("Please enter your name before submitting.");
      return;
    }

    if (answer.trim().length < 10) {
      setMessage("Please write an answer of at least 10 characters.");
      return;
    }

    setSubmitting(true);
    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/answers/submit",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            candidate_name: candidateName.trim(),
            role: interview.role,
            question: interview.questions[currentQuestion],
            answer: answer.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Answer submission failed.");
      }

      const evaluation = data.evaluation;

      if (
        !evaluation ||
        typeof evaluation.predicted_score !== "number"
      ) {
        throw new Error("The backend did not return a valid ML score.");
      }

      const newResult: EvaluationResult = {
        question: interview.questions[currentQuestion],
        predicted_score: evaluation.predicted_score,
        maximum_score: evaluation.maximum_score,
        evaluation_type: evaluation.evaluation_type,
      };

      setEvaluationResults((previous) => [...previous, newResult]);

      if (currentQuestion === interview.questions.length - 1) {
        setCompleted(true);
        setMessage("All answers evaluated successfully!");
      } else {
        setCurrentQuestion((previous) => previous + 1);
        setAnswer("");
        setMessage("Answer evaluated successfully!");
      }
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Could not submit your answer."
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <main className="session-page">Loading interview...</main>;
  }

  if (!interview) {
    return (
      <main className="session-page">
        <div className="session-card">
          <h2>Interview not available</h2>
          <p>{message}</p>
          <a href="/interview" className="session-button">
            Configure Interview
          </a>
        </div>
      </main>
    );
  }

  if (completed) {
    const totalScore = evaluationResults.reduce(
      (total, result) => total + result.predicted_score,
      0
    );

    const averageScore =
      evaluationResults.length > 0
        ? totalScore / evaluationResults.length
        : 0;

    return (
      <main className="session-page">
        <div className="session-card completion-card">
          <div className="completion-icon">✓</div>

          <h1>Interview completed!</h1>

          <p>
            Congratulations, {candidateName}! You submitted all{" "}
            {interview.questions.length} answers.
          </p>

          <div className="evaluation-summary">
            <div className="score-label">YOUR AVERAGE ML SCORE</div>

            <div className="average-score">
              {averageScore.toFixed(2)}
              <span> / 10</span>
            </div>

            <p>
              Based on {evaluationResults.length} evaluated answers
            </p>
          </div>

          <h2 className="results-heading">Question-wise results</h2>

          <div className="results-list">
            {evaluationResults.map((result, index) => (
              <div className="result-item" key={index}>
                <div className="result-question">
                  <span>QUESTION {index + 1}</span>
                  <p>{result.question}</p>
                </div>

                <div className="result-score">
                  {result.predicted_score.toFixed(2)}
                  <span> / {result.maximum_score}</span>
                </div>
              </div>
            ))}
          </div>

          <p className="session-notice">
            These scores are experimental predictions from your
            PyTorch model. They are not yet validated assessments
            of answer quality.
          </p>

          <a href="/" className="session-button">
            Return to Dashboard →
          </a>
        </div>
      </main>
    );
  }

  const progress =
    ((currentQuestion + 1) / interview.questions.length) * 100;

  return (
    <main className="session-page">
      <header className="session-header">
        <a href="/" className="back-link">
          ← Exit Interview
        </a>

        <span className="setup-status">
          <i /> LIVE INTERVIEW SESSION
        </span>
      </header>

      <section className="session-container">
        <div className="session-heading">
          <div className="eyebrow">YOUR PERSONAL AI INTERVIEWER</div>
          <h1>
            Show what <span>you know.</span>
          </h1>
          <p>
            {interview.role} · {interview.difficulty} difficulty
          </p>
        </div>

        <div className="session-card">
          <div className="session-top">
            <span>
              QUESTION {currentQuestion + 1} OF{" "}
              {interview.questions.length}
            </span>

            <span>{Math.round(progress)}% COMPLETE</span>
          </div>

          <div className="session-progress">
            <div style={{ width: `${progress}%` }} />
          </div>

          <div className="question-label">INTERVIEW QUESTION</div>

          <h2 className="question-text">
            {interview.questions[currentQuestion]}
          </h2>

          <div className="candidate-field">
            <label htmlFor="candidate">YOUR NAME</label>

            <input
              id="candidate"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              placeholder="Enter your name"
              disabled={currentQuestion > 0}
            />
          </div>

          <div className="answer-field">
            <label htmlFor="answer">YOUR ANSWER</label>

            <textarea
              id="answer"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Explain your answer clearly. Include examples where possible..."
              rows={9}
            />

            <span>
              {answer.trim().split(/\s+/).filter(Boolean).length} words
            </span>
          </div>

          {message && (
            <p className="session-message" role="status">
              {message}
            </p>
          )}

          <button
            className="session-button"
            onClick={submitAnswer}
            disabled={submitting}
          >
            {submitting
              ? "Evaluating your answer..."
              : currentQuestion === interview.questions.length - 1
                ? "Finish Interview"
                : "Submit & Next Question"}

            <span>→</span>
          </button>

          <p className="session-notice">
            Your answer will be evaluated using the trained
            experimental ML model.
          </p>
        </div>
      </section>
    </main>
  );
}
