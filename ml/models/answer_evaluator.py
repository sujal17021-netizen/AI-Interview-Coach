
import torch
import torch.nn as nn


class AnswerEvaluator(nn.Module):

    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(

            # Input: 384-dimensional embedding
            nn.Linear(384, 128),
            nn.ReLU(),

            # Hidden layer
            nn.Linear(128, 64),
            nn.ReLU(),

            # Output: predicted score
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.network(x)
