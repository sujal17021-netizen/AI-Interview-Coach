
# AI Interview Coach 🎯

An AI-powered interview preparation platform designed to help candidates practice technical interviews, evaluate their answers, and improve their interview performance using Machine Learning, Deep Learning, and Large Language Models.

## 🚀 Project Overview

AI Interview Coach provides an interactive interview environment where candidates can select their job role, difficulty level, answer interview questions, and receive automated evaluation.

The platform uses Sentence Transformers and a PyTorch neural network for experimental answer scoring, with plans to integrate LLM-powered feedback and Retrieval-Augmented Generation (RAG).

## ✨ Features

- Interactive interview sessions
- Role-based interview questions
- Configurable difficulty levels
- Answer submission through FastAPI
- Sentence Transformer embeddings
- PyTorch-based answer evaluation
- Question-wise predicted scores
- Average interview score
- Modern Next.js dashboard

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Backend | Python, FastAPI |
| Machine Learning | PyTorch |
| NLP / Embeddings | Sentence Transformers |
| Dataset Processing | Pandas, NumPy |
| LLM Integration | Google Gemini |
| Vector Database | ChromaDB |

## 🏗️ Project Structure

```text
AI-Interview-Coach/
├── backend/
│   └── app/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       └── main.py
├── frontend/
│   └── app/
├── ml/
│   ├── models/
│   ├── training/
│   ├── evaluation/
│   └── embeddings/
├── dataset/
│   ├── raw/
│   ├── processed/
│   └── generated/
├── knowledge_base/
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Interview-Coach
```

### 2. Backend setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi uvicorn torch sentence-transformers scikit-learn pandas numpy python-dotenv google-genai chromadb
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
```

Start the backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Backend documentation:

http://127.0.0.1:8000/docs

### 3. Frontend setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

http://localhost:3000

## 🧠 Machine Learning Workflow

1. Collect and prepare interview answer datasets.
2. Generate semantic embeddings using Sentence Transformers.
3. Train a PyTorch neural network.
4. Load the trained model into the FastAPI backend.
5. Evaluate submitted answers.
6. Return experimental predicted scores to the frontend.

## 🔮 Future Enhancements

- Gemini-powered answer feedback
- Resume parsing and personalization
- Retrieval-Augmented Generation (RAG)
- Adaptive interview difficulty
- Voice-based interviews
- PostgreSQL database integration
- Candidate performance analytics
- Personalized learning recommendations

## ⚠️ Current Limitations

The current PyTorch evaluator is experimental and trained on a small dataset. Its predicted scores should not be treated as reliable assessments of candidate ability.

## 👨‍💻 Author

Sujal Gupta

AI Interview Coach — An ongoing full-stack AI/ML project.
