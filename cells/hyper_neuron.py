import math
import random
import json
import os

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-max(min(x, 500), -500)))

def sigmoid_derivative(y):
    return y * (1.0 - y)

class HyperNeuron:
    def __init__(self, cell_id, n_inputs=4, storage_dir="synapses"):
        self.id = cell_id
        self.n_inputs = n_inputs
        self.storage_path = os.path.join(storage_dir, f"{self.id}.json")
        self.os_dir = storage_dir
        
        self.weights = []
        self.bias = 0.0
        self.last_inputs = []
        self.last_out = 0.0
        
        self.load_self()

    def load_self(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                if len(data.get("w", [])) == self.n_inputs:
                    self.weights = data["w"]
                    self.bias = data.get("b", 0.0)
                    return
            except Exception: pass

        self.weights = [random.uniform(-1.0, 1.0) for _ in range(self.n_inputs)]
        self.bias = random.uniform(-0.5, 0.5)
        self.save_self()

    def forward(self, inputs):
        self.last_inputs = inputs
        s = sum(inputs[i] * self.weights[i] for i in range(self.n_inputs)) + self.bias
        self.last_out = sigmoid(s)
        return self.last_out

    def backward(self, delta, lr=0.1):
        for i in range(self.n_inputs):
            self.weights[i] += lr * delta * self.last_inputs[i]
        self.bias += lr * delta
        self.save_self()

    def save_self(self):
        os.makedirs(self.os_dir, exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"w": [round(w, 4) for w in self.weights], "b": round(self.bias, 4)}, f, indent=4)
