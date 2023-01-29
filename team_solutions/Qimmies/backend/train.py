import csv
import pennylane as qml
from pennylane import numpy as np
import covalent as ct
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
from sklearn.kernel_approximation import Nystroem
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load
from kernel import *
import nltk

def extract_features(sample):
    sample_words = set(sample[0])
    features = {}
    for word in sample[1]:
        features['contains(%s)' % word] = (word in sample_words)
    return features

@ct.electron(
    files=[
        ct.fs.FileTransfer(ct.fs.File("~/Documents/Projects/iQuHACK/SmallDataSet.csv"), ct.fs.File("SmallDataSet.csv"), ct.fs.Order.BEFORE, None),
        ct.fs.FileTransfer(ct.fs.File("~/Documents/Projects/iQuHACK/backend/kernel.py"), ct.fs.File("kernel.py"), ct.fs.Order.BEFORE, None)
    ]
)
def get_data(files):
    word_freq = {}
    word_list = []
    samples = []
    s_idx = 0
    max_data = 200
    with open("SmallDataSet.csv") as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            s_idx += 1
            if (s_idx > max_data and s_idx < 1000) or s_idx > 1000 + max_data:
                continue
            words = row[1].split()
            samples.append(((words, word_list), row[0]))
            for word in words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
        word_list.extend(sorted(word_freq))
        training_set = nltk.classify.apply_features(extract_features, samples)
    
    vectorizer = DictVectorizer(dtype=float, sparse=False)
    encoder = LabelEncoder()
    X, y = list(zip(*training_set))
    X = vectorizer.fit_transform(X)
    y = encoder.fit_transform(y)
    return X, y, vectorizer, encoder, word_list, len(vectorizer.feature_names_)

@ct.electron
def split_train_test_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=3)
    return X_train, X_test, y_train, y_test

@ct.electron
def init_params(num_wires, feature_count):
    return np.random.uniform(0, 2 * np.pi, (feature_count // num_wires, 2, num_wires), requires_grad=True)

@ct.electron
def svm(X, y, params):
    kernel_input = lambda x1, x2: kernel(x1, x2, params)
    svm = SVC(kernel=lambda x1, x2: qml.kernels.kernel_matrix(x1, x2, kernel_input), probability=True)
    svm.fit(X, y)
    return svm

@ct.electron
def calc_accuracy(classifier, X, y_true):
    return 1 - np.count_nonzero(classifier.predict(X) - y_true) / len(y_true)

def target_alignment(
    X,
    Y,
    kernel,
    assume_normalized_kernel=False,
    rescale_class_labels=True,
):
    K = qml.kernels.square_kernel_matrix(
        X,
        kernel,
        assume_normalized_kernel=assume_normalized_kernel,
    )

    if rescale_class_labels:
        nplus = np.count_nonzero(np.array(Y) == 1)
        nminus = len(Y) - nplus
        _Y = np.array([y / nplus if y == 1 else y / nminus for y in Y])
    else:
        _Y = np.array(Y)

    T = np.outer(_Y, _Y)
    inner_product = np.sum(K * T)
    norm = np.sqrt(np.sum(K * K) * np.sum(T * T))
    inner_product = inner_product / norm

    return inner_product

@ct.electron
def get_optimizer():
    return qml.GradientDescentOptimizer(0.4)
    #return qml.AdagradOptimizer(0.4)

@ct.electron
def training(X, Y, init_params, opt, steps):
    params = init_params
    KTAs = []
    for i in range(steps):
        # Randomly choose subset of data points to compute the KTA on.
        subset = np.random.choice(list(range(len(X))), 5)
        # Define the cost function for optimization
        cost = lambda _params: -target_alignment(
            X[subset],
            Y[subset],
            lambda x1, x2: kernel(x1, x2, _params),
            assume_normalized_kernel=True,
        )
        # Optimization step
        params = opt.step(cost, params)
        KTAs.append(
            target_alignment(
                X, Y, lambda x1, x2: kernel(x1, x2, params), assume_normalized_kernel=True
            )
        )

    return params, KTAs

@ct.lattice
def trained_qsvm(num_wires=5, steps=300):
    X, y, vectorizer, encoder, word_list, feature_count = get_data()
    X_train, X_test, y_train, y_test = split_train_test_data(X, y)
    params = init_params(num_wires, feature_count)
    opt = get_optimizer()
    opt_params, KTAs = training(X_train, y_train, params, opt, steps)
    opt_classifier = svm(X_train, y_train, opt_params)
    train_acc = calc_accuracy(classifier=opt_classifier, X=X_train, y_true=y_train)
    test_acc = calc_accuracy(classifier=opt_classifier, X=X_test, y_true=y_test)
    return opt_classifier, opt_params, train_acc, test_acc, vectorizer, encoder, word_list

if __name__ == "__main__":
    dispatch_id = ct.dispatch(trained_qsvm)(5, 3)
    result = ct.get_result(dispatch_id=dispatch_id, wait=True)
    opt_qsvm, opt_params, train_acc, test_acc, vectorizer, encoder, word_list = result.result

    opt_qsvm.kernel = None
    dump(opt_qsvm, 'trained_model.joblib') 
    dump(opt_params, 'trained_params.joblib') 
    dump(vectorizer, 'trained_vectorizer.joblib') 
    dump(encoder, 'trained_encoder.joblib') 
    dump(word_list, 'trained_wordlist.joblib') 