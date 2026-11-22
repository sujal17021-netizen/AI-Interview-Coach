
import numpy as np
import torch
import torch.nn as nn

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from ml.models.answer_evaluator import AnswerEvaluator

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

EMBEDDING_PATH = BASE_DIR / "dataset" / "processed" / "answer_embeddings.npy"
SCORE_PATH = BASE_DIR / "dataset" / "processed" / "answer_scores.npy"
MODEL_PATH = BASE_DIR / "ml" / "models" / "answer_evaluator.pth"

# Load dataset
print("Loading dataset...")

X = np.load(EMBEDDING_PATH)
y = np.load(SCORE_PATH)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

results = []

# 1. Linear Regression
print("\nTraining Linear Regression...")

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

linear_predictions = np.clip(linear_model.predict(X_test), 0, 10)

results.append((
    "Linear Regression",
    mean_absolute_error(y_test, linear_predictions),
    np.sqrt(mean_squared_error(y_test, linear_predictions))
))

# 2. Random Forest
print("Training Random Forest...")

forest_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
forest_model.fit(X_train, y_train)

forest_predictions = np.clip(forest_model.predict(X_test), 0, 10)

results.append((
    "Random Forest",
    mean_absolute_error(y_test, forest_predictions),
    np.sqrt(mean_squared_error(y_test, forest_predictions))
))

# 3. Existing Neural Network
print("Evaluating Neural Network...")

neural_model = AnswerEvaluator()
neural_model.load_state_dict(
    torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
)
neural_model.eval()

X_test_tensor = torch.tensor(X_test, dtype=torch.float32)

with torch.no_grad():
    neural_predictions = neural_model(X_test_tensor).numpy().flatten()

neural_predictions = np.clip(neural_predictions, 0, 10)

results.append((
    "Neural Network",
    mean_absolute_error(y_test, neural_predictions),
    np.sqrt(mean_squared_error(y_test, neural_predictions))
))

# Display comparison
print("\n========== MODEL COMPARISON ==========")
print(f"{'Model':<22} {'MAE':<12} {'RMSE':<12}")

for name, mae, rmse in results:
    print(f"{name:<22} {mae:<12.4f} {rmse:<12.4f}")

print("\nLower MAE and RMSE indicate better predictions.")
