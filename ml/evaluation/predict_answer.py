
import torch
from sentence_transformers import SentenceTransformer

from ml.models.answer_evaluator import AnswerEvaluator

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

print("Loading trained evaluator...")

model = AnswerEvaluator()

model_path = "ml/models/answer_evaluator.pth"

model.load_state_dict(
    torch.load(model_path, map_location="cpu", weights_only=True)
)

model.eval()

question = "What is overfitting in machine learning?"

answer = """
Overfitting happens when a machine learning model learns the
training data too closely, including noise and unnecessary details.
As a result, it performs well on training data but poorly on
unseen test data. Regularization, cross-validation and more
training data can help reduce overfitting.
"""

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
    predicted_score = model(input_tensor).item()

predicted_score = max(0, min(10, predicted_score))

print("\n========== INTERVIEW EVALUATION ==========")
print("Question:", question)
print("Answer:", answer)
print(f"Predicted score: {predicted_score:.2f}/10")
