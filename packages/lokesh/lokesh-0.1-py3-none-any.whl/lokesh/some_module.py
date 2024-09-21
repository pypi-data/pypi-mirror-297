 
# lokesh/some_module.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier

class SimpleModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
