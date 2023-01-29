import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from qiskit import QuantumCircuit
from qiskit.algorithms.optimizers import COBYLA, L_BFGS_B
from qiskit.circuit import Parameter
from qiskit.circuit.library import RealAmplitudes, ZZFeatureMap
from qiskit.utils import algorithm_globals
from qiskit_machine_learning.algorithms.classifiers import (
    VQC, NeuralNetworkClassifier)
from qiskit_machine_learning.algorithms.regressors import (
    VQR, NeuralNetworkRegressor)
from qiskit_machine_learning.neural_networks import EstimatorQNN, SamplerQNN

algorithm_globals.random_seed = 42

num_inputs = 2
num_samples = 20

X = 2 * np.random.rand(num_samples, num_inputs) - 1
y = np.random.choice([0, 1, 2], 100) 
y_one_hot = np.zeros((num_samples, 3))

for i in range(num_samples):
    y_one_hot[i, y[i]] = 1

for x, y_target in zip(X, y):
    if y_target == 1:
        plt.plot(x[0], x[1], "bo")
    else:
        plt.plot(x[0], x[1], "go")
plt.plot([-1, 0, 1], [1, 0, -1], "--", color="black")
plt.show()

# construct QNN
qc = QuantumCircuit(2)
feature_map = ZZFeatureMap(2)
ansatz = RealAmplitudes(2)
qc.compose(feature_map, inplace=True)
qc.compose(ansatz, inplace=True)
qc.draw(output="mpl")

