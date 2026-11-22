
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

from ml.models.answer_evaluator import AnswerEvaluator

BASE_DIR = Path(__file__).resolve().parents[2]

EMBEDDING_PATH = BASE_DIR / "dataset" / "processed" / "validated_embeddings.npy"
SCORE_PATH = BASE_DIR / "dataset" / "processed" / "validated_scores.npy"
MODEL_PATH = BASE_DIR / "ml" / "models" / "answer_evaluator.pth"

print("Loading human-validated data...")

X = np.load(EMBEDDING_PATH)
y = np.load(SCORE_PATH)

print("Embedding shape:", X.shape)
print("Score shape:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

model = AnswerEvaluator()

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 100

print("\nTraining model...")

for epoch in range(epochs):
    model.train()

    predictions = model(X_train)
    loss = criterion(predictions, y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

print("\nEvaluating model...")

model.eval()

with torch.no_grad():
    predictions = model(X_test)

    mae = mean_absolute_error(
        y_test.numpy(),
        predictions.numpy()
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test.numpy(),
            predictions.numpy()
        )
    )

print("\n========== MODEL EVALUATION ==========")
print(f"Test MAE: {mae:.4f}")
print(f"Test RMSE: {rmse:.4f}")

torch.save(model.state_dict(), MODEL_PATH)

print("\nModel saved:", MODEL_PATH)
