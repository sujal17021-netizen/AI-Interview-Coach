
"use client";

import { useEffect, useState } from "react";

// Interview question structure
type InterviewQuestion = {
  question: string;
  category: "Technical" | "HR";
};

// Interview configuration structure
type InterviewData = {
  role: string;
  difficulty: string;
  interview_type: string;
  duration: number;
  total_questions: number;
  generation_source: string;
  questions: InterviewQuestion[];
};

// Gemini AI evaluation structure
type AIEvaluation = {
  technical_accuracy: number;
  relevance: number;
  completeness: number;
  clarity: number;
  strengths: string[];
  improvements: string[];
  improved_answer: string;
  overall_feedback: string;
};

// Individual question evaluation structure
type EvaluationResult = {
  question: string;
  category: string;
  predicted_score: number;
  maximum_score: number;
  evaluation_type: string;
  ai_evaluation: AIEvaluation | null;
};

export default function InterviewSession() {
  const [interview, setInterview] =
    useState<InterviewData | null>(null);

  const [candidateName, setCandidateName] = useState("");
  const [answer, setAnswer] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [message, setMessage] = useState("");
  const [completed, setCompleted] = useState(false);

  const [evaluationResults, setEvaluationResults] =
    useState<EvaluationResult[]>([]);

  // Load interview questions from sessionStorage
  useEffect(() => {
    const saved = sessionStorage.getItem("interviewQuestions");

    if (saved) {
      try {
        const parsed = JSON.parse(saved);

        if (
          !parsed ||
          !Array.isArray(parsed.questions) ||
          parsed.questions.length === 0 ||
          !parsed.questions.every(
            (q: unknown) =>
              typeof q === "object" &&
              q !== null &&
              "question" in q &&
              "category" in q &&
              typeof q.question === "string" &&
              (q.category === "Technical" ||
                q.category === "HR")
          )
        ) {
          throw new Error("Invalid question format.");
        }

        setInterview(parsed);
      } catch {
        setMessage(
          "Invalid interview data. Please start a new interview."
        );
      }
    } else {
      setMessage(
        "No interview found. Please configure a new interview."
      );
    }

    setLoading(false);
  }, []);

  // Submit candidate answer
  async function submitAnswer() {
    if (!interview) return;

    if (candidateName.trim().length < 2) {
      setMessage("Please enter your name before submitting.");
      return;
    }

    if (answer.trim().length < 10) {
      setMessage(
        "Please write an answer of at least 10 characters."
      );
      return;
    }

    setSubmitting(true);
    setMessage("");

    const questionItem = interview.questions[currentQuestion];

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
            question: questionItem.question,
            answer: answer.trim(),
            category: questionItem.category,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Answer submission failed."
        );
      }

      // Read both evaluation results
      const evaluation = data.evaluation;

      if (
        !evaluation ||
        !evaluation.ml_evaluation ||
        typeof evaluation.ml_evaluation.predicted_score !==
          "number"
      ) {
        throw new Error(
          "The backend did not return a valid ML score."
        );
      }

      const mlEvaluation = evaluation.ml_evaluation;

      // Gemini feedback may be unavailable if the API fails
      const rawAI = evaluation.ai_evaluation;

      const aiEvaluation: AIEvaluation | null =
        rawAI &&
        typeof rawAI.technical_accuracy === "number" &&
        typeof rawAI.relevance === "number" &&
        typeof rawAI.completeness === "number" &&
        typeof rawAI.clarity === "number" &&
        Array.isArray(rawAI.strengths) &&
        Array.isArray(rawAI.improvements) &&
        typeof rawAI.improved_answer === "string" &&
        typeof rawAI.overall_feedback === "string"
          ? rawAI as AIEvaluation
          : null;

      // Store question-wise results
      const newResult: EvaluationResult = {
        question: questionItem.question,
        category: questionItem.category,
        predicted_score: mlEvaluation.predicted_score,
        maximum_score: mlEvaluation.maximum_score,
        evaluation_type: mlEvaluation.evaluation_type,
        ai_evaluation: aiEvaluation,
      };

      setEvaluationResults((previous) => [
        ...previous,
        newResult,
      ]);

      // Move to next question or complete interview
      if (
        currentQuestion === interview.questions.length - 1
      ) {
        setCompleted(true);
        setMessage("All answers evaluated successfully!");
      } else {
        setCurrentQuestion((previous) => previous + 1);
        setAnswer("");

        setMessage(
          aiEvaluation
            ? "Answer evaluated successfully!"
            : "Answer saved. AI feedback was unavailable for this answer."
        );
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

  // Loading screen
  if (loading) {
    return (
      <main className="session-page">
        Loading interview...
      </main>
    );
  }

  // Interview unavailable screen
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

  // Calculate and display final results
  if (completed) {
    const totalScore = evaluationResults.reduce(
      (total, result) =>
        total + result.predicted_score,
      0
    );

    const averageScore =
      evaluationResults.length > 0
        ? totalScore / evaluationResults.length
        : 0;

    const aiResults = evaluationResults.filter(
      (result) => result.ai_evaluation !== null
    );

    const averageAI = (field: keyof AIEvaluation) => {
      if (aiResults.length === 0) return null;

      const total = aiResults.reduce((sum, result) => {
        const value = result.ai_evaluation?.[field];

        return sum +
          (typeof value === "number" ? value : 0);
      }, 0);

      return (total / aiResults.length).toFixed(2);
    };

    return (
      <main className="session-page">
        <div className="session-card completion-card">

          <div className="completion-icon">✓</div>

          <h1>Interview completed!</h1>

          <p>
            Congratulations, {candidateName}! You submitted all{" "}
            {interview.questions.length} answers.
          </p>

          {/* PyTorch average score */}
          <div className="evaluation-summary">
            <div className="score-label">
              YOUR AVERAGE ML SCORE
            </div>

            <div className="average-score">
              {averageScore.toFixed(2)}
              <span> / 10</span>
            </div>

            <p>
              Based on {evaluationResults.length} evaluated answers
            </p>
          </div>

          {/* Gemini overall summary */}
          <div className="evaluation-summary">
            <div className="score-label">
              YOUR AVERAGE AI SCORES
            </div>

            {aiResults.length > 0 ? (
              <div className="ai-scores">
                <p>
                  Technical Accuracy / Authenticity
                  <strong>
                    {averageAI("technical_accuracy")}/10
                  </strong>
                </p>

                <p>
                  Relevance
                  <strong>
                    {averageAI("relevance")}/10
                  </strong>
                </p>

                <p>
                  Completeness
                  <strong>
                    {averageAI("completeness")}/10
                  </strong>
                </p>

                <p>
                  Clarity
                  <strong>
                    {averageAI("clarity")}/10
                  </strong>
                </p>
              </div>
            ) : (
              <p>
                AI feedback was unavailable for these answers.
              </p>
            )}

            <p>
              Gemini evaluated {aiResults.length} of{" "}
              {evaluationResults.length} answers.
            </p>
          </div>

          <h2 className="results-heading">
            Question-wise results
          </h2>

          <div className="results-list">
            {evaluationResults.map((result, index) => (
              <div className="result-item" key={index}>

                {/* Question */}
                <div className="result-question">
                  <span>
                    QUESTION {index + 1} ·{" "}
                    {result.category.toUpperCase()}
                  </span>

                  <p>{result.question}</p>
                </div>

                {/* PyTorch score */}
                <div className="result-score">
                  {result.predicted_score.toFixed(2)}
                  <span> / {result.maximum_score}</span>
                </div>

                {/* Gemini feedback */}
                {result.ai_evaluation && (
                  <div className="ai-feedback">

                    <h3>Gemini AI Feedback</h3>

                    {/* Four evaluation scores */}
                    <div className="ai-scores">

                      <p>
                        {result.category === "HR"
    ? "Authenticity"
    : "Technical Accuracy"}
                        <strong>
                          {result.ai_evaluation.technical_accuracy}/10
                        </strong>
                      </p>

                      <p>
                        Relevance
                        <strong>
                          {result.ai_evaluation.relevance}/10
                        </strong>
                      </p>

                      <p>
                        Completeness
                        <strong>
                          {result.ai_evaluation.completeness}/10
                        </strong>
                      </p>

                      <p>
                        Clarity
                        <strong>
                          {result.ai_evaluation.clarity}/10
                        </strong>
                      </p>

                    </div>

                    {/* Strengths */}
                    <h4>Strengths</h4>

                    <ul>
                      {result.ai_evaluation.strengths.map(
                        (item, i) => (
                          <li key={i}>{item}</li>
                        )
                      )}
                    </ul>

                    {/* Improvements */}
                    <h4>Areas for Improvement</h4>

                    <ul>
                      {result.ai_evaluation.improvements.map(
                        (item, i) => (
                          <li key={i}>{item}</li>
                        )
                      )}
                    </ul>

                    {/* Improved answer */}
                    <h4>Suggested Improved Answer</h4>

                    <p>
                      {result.ai_evaluation.improved_answer}
                    </p>

                    {/* Overall feedback */}
                    <h4>Overall Feedback</h4>

                    <p>
                      {result.ai_evaluation.overall_feedback}
                    </p>

                  </div>
                )}

                {!result.ai_evaluation && (
                  <div className="ai-feedback">
                    <h3>AI Feedback Unavailable</h3>
                    <p>
                      Gemini could not evaluate this answer.
                      The experimental ML score is still available.
                    </p>
                  </div>
                )}

              </div>
            ))}
          </div>

          {/* ML disclaimer */}
          <p className="session-notice">
            PyTorch scores are experimental predictions from your
            trained model. They are not yet validated assessments
            of answer quality. Gemini feedback is AI-generated and
            should also be reviewed critically.
          </p>

          <a href="/" className="session-button">
            Return to Dashboard →
          </a>

        </div>
      </main>
    );
  }

  // Active interview screen
  const questionItem = interview.questions[currentQuestion];

  const progress =
    ((currentQuestion + 1) /
      interview.questions.length) *
    100;

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

          <div className="eyebrow">
            YOUR PERSONAL AI INTERVIEWER
          </div>

          <h1>
            Show what <span>you know.</span>
          </h1>

          <p>
            {interview.role} · {interview.difficulty} difficulty
          </p>

        </div>

        <div className="session-card">

          {/* Question progress */}
          <div className="session-top">

            <span>
              QUESTION {currentQuestion + 1} OF{" "}
              {interview.questions.length}
            </span>

            <span>
              {Math.round(progress)}% COMPLETE
            </span>

          </div>

          <div className="session-progress">
            <div style={{ width: `${progress}%` }} />
          </div>

          {/* Question category */}
          <div className="question-label">
            INTERVIEW QUESTION
          </div>

          <div className="question-category">
            {questionItem.category === "Technical"
              ? "💻 TECHNICAL QUESTION"
              : "👤 HR QUESTION"}
          </div>

          {/* Question text */}
          <h2 className="question-text">
            {questionItem.question}
          </h2>

          {/* Candidate name */}
          <div className="candidate-field">

            <label htmlFor="candidate">
              YOUR NAME
            </label>

            <input
              id="candidate"
              value={candidateName}
              onChange={(e) =>
                setCandidateName(e.target.value)
              }
              placeholder="Enter your name"
              disabled={currentQuestion > 0}
            />

          </div>

          {/* Candidate answer */}
          <div className="answer-field">

            <label htmlFor="answer">
              YOUR ANSWER
            </label>

            <textarea
              id="answer"
              value={answer}
              onChange={(e) =>
                setAnswer(e.target.value)
              }
              placeholder="Explain your answer clearly. Include examples where possible..."
              rows={9}
            />

            <span>
              {answer.trim().split(/\s+/).filter(Boolean).length} words
            </span>

          </div>

          {/* Status messages */}
          {message && (
            <p className="session-message" role="status">
              {message}
            </p>
          )}

          {/* Submit button */}
          <button
            className="session-button"
            onClick={submitAnswer}
            disabled={submitting}
          >
            {submitting
              ? "Evaluating your answer..."
              : currentQuestion ===
                  interview.questions.length - 1
                ? "Finish Interview"
                : "Submit & Next Question"}

            <span>→</span>
          </button>

          <p className="session-notice">
            Your answer will be evaluated using the experimental
            PyTorch model and Gemini AI.
          </p>

        </div>

      </section>

    </main>
  );
}
