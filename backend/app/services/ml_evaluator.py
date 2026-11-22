
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer

from ml.models.answer_evaluator import AnswerEvaluator


BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "ml" / "models" / "answer_evaluator.pth"

# Load embedding model once when the service starts
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

# Load trained PyTorch model
evaluator = AnswerEvaluator()

evaluator.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True
    )
)

evaluator.eval()


def evaluate_answer(question: str, answer: str):
    text = f"Question: {question} Answer: {answer}"

    embedding = embedding_model.encode(
        [text],
        convert_to_numpy=True
    )

    input_tensor = torch.tensor(
        embedding,
        dtype=torch.float32
    )

    with torch.no_grad():
        prediction = evaluator(input_tensor).item()

    score = max(0.0, min(10.0, prediction))

    return {
        "predicted_score": round(score, 2),
        "maximum_score": 10,
        "evaluation_type": "Experimental PyTorch model"
    }
