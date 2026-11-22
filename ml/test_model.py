
import torch
from ml.models.answer_evaluator import AnswerEvaluator

model = AnswerEvaluator()

# Create a sample embedding
sample_input = torch.randn(1, 384)

# Make prediction
output = model(sample_input)

print("Input shape:", sample_input.shape)
print("Output shape:", output.shape)
print("Predicted score:", output.item())
