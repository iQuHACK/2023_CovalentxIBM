import numpy as np
import covalent as ct
import csv
from sklearn import decomposition
import pickle as pk
# Import for SVM classifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
# Imports for QSVC classifier
from qiskit import BasicAer
from qiskit.circuit.library import ZZFeatureMap
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_machine_learning.kernels import QuantumKernel
# Import plotting library
import matplotlib.pyplot as plt
plt.rcParams["figure.facecolor"] = "w"

# Set the random seed for QSVC
seed = 12345
algorithm_globals.random_seed = seed

# token to access IBM Quantum compute resources
IBM_QUANTUM_TOKEN = "123456789qwertyuiopzxcvbnmasdfghjkl"


def read_data(file_name, target_features=5, pca_filename="data/pca.pkl"):
    """
    Based off of Brown CSCI 1420

    Reads the data from the input file and splits it into normalized inputs
    and labels. Runs PCA to reduce the feature space, and saves fitted PCA object

    :param file_name: path to the desired data file
    :return: two numpy arrays, one containing the inputs and one containing
              the labels
    """
    inputs, labels, classes = [], [], set()
    with open(file_name) as f:
        positive_label = None
        reader = csv.reader(f)
        for row in reader:
            example = np.array(row)
            classes.add(example[-1])
            # our datasets all start with a True example
            if positive_label is None:
                positive_label = example[-1]
            # converting data points to labels of [-1, 1]
            label = 1 if example[-1] == positive_label else -1
            row.pop()
            labels.append(label)
            inputs.append([float(val) for val in row])

    if len(classes) > 2:
        print('Only binary classification tasks are supported.')
        exit()

    inputs = np.array(inputs)
    labels = np.array(labels)

    # Normalize the feature values
    for j in range(inputs.shape[1]):
        col = inputs[:, j]
        mu = np.mean(col)
        sigma = np.std(col)
        if sigma == 0: sigma = 1
        inputs[:, j] = 1 / sigma * (col - mu)

    pca = decomposition.PCA(n_components=target_features)
    pca.fit(inputs)
    inputs = pca.transform(inputs)

    with open(pca_filename, "wb") as fd:
        pk.dump(pca, fd)

    return inputs, labels


# Ancillary functions for SVM classifiers
@ct.electron
def get_data(nsize=100):
    X, y = read_data("./data/spambase.csv")
    rand = np.random.permutation(len(y))
    X = X[rand]
    y = y[rand]
    return X[:nsize], y[:nsize]


@ct.electron
def split_train_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    return X_train, X_test, y_train, y_test


@ct.electron
def train_svc(X_train, y_train):
    svc = SVC(kernel="linear")
    svc.fit(X_train, y_train)
    return svc


@ct.electron
def train_qsvc(X_train, y_train):
    feature_map = ZZFeatureMap(5)
    backend = QuantumInstance(
        BasicAer.get_backend("qasm_simulator"), shots=100, seed_simulator=seed, seed_transpiler=seed
    )
    kernel = QuantumKernel(feature_map=feature_map, quantum_instance=backend)
    qsvc = SVC(kernel=kernel.evaluate)
    qsvc.fit(X_train, y_train)
    return qsvc


# Main Workflow
@ct.lattice
def workflow():
    X, y = get_data()
    X_train, X_test, y_train, y_test = split_train_test(X=X, y=y)
    svc_model = train_svc(X_train=X_train, y_train=y_train)
    qsvc_model = train_qsvc(X_train=X_train, y_train=y_train)
    return X_test, y_test, svc_model, qsvc_model


# Dispatch workflow and obtain results
dispatch_id = ct.dispatch(workflow)()
result = ct.get_result(dispatch_id=dispatch_id, wait=True)
result = workflow()

# Save results
X_test, y_test, svc_model, qsvc_model = result
with open("models/svc.pkl", "wb") as fd:
    pk.dump(svc_model, fd)
with open("models/qsvc.pkl", "wb") as fd:
    pk.dump(qsvc_model, fd)
