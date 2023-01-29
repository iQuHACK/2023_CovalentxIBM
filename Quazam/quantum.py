from qiskit import IBMQ
# from app import *
from sklearn.model_selection import train_test_split
from qiskit.utils import algorithm_globals
from qiskit.circuit.library import ZZFeatureMap
from qiskit.primitives import Sampler
from qiskit.algorithms.state_fidelities import ComputeUncompute
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from sklearn import preprocessing
from sklearn.svm import SVC
import pandas as pd
def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

IBMQ.save_account('4b591e521ffb6135df4fd4dbed1f04a59ca81bc6d5b206436c22e2f02623cf6cf3efd5cd8d00f8b4c6deae9b6b0384fae3456f735772b340b78009b5ba1752ff', overwrite = 'True')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q-community')
backend = provider.get_backend('ibm_nairobi')

netflix = pd.read_csv("static/netflix.csv")
netflix = swap_columns(netflix, "Today", "Sentiment_Score")
print(netflix)
X = netflix.iloc[:, :7] # 8 parameters
y = netflix.iloc[:, 7]
lab = preprocessing.LabelEncoder()
y_transformed = lab.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

algorithm_globals.random_seed = 12345

feature_dim = 7
feature_map = ZZFeatureMap(feature_dimension=feature_dim, reps=10,entanglement="linear")

sampler = Sampler()
fidelity = ComputeUncompute(sampler=sampler)

kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)

train_features = []
train_labels = []
svc = SVC(kernel=kernel.evaluate)
svc.fit(X_train, y_train)

score_callable_function = svc.score(X_test, y_test)

print(f"Callable kernel classification test score: {score_callable_function}")

