
from fastapi import FastAPI
from backend.app.routes.interviews import router as interviews_router
from backend.app.routes.questions import router as questions_router
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.answers import router as answers_router
app = FastAPI(
    title="AI Interview Coach",
    description="An AI-powered interview preparation platform using ML, RAG and LLMs.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(questions_router)
app.include_router(answers_router)
app.include_router(interviews_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Interview Coach!",
        "status": "Backend is running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI Interview Coach"
    }
