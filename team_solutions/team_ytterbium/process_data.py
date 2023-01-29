import numpy as np
import matplotlib.pyplot as plt
from sklearn import decomposition
from sklearn import datasets
import csv


def read_data(file_name, target_features=5):
    """
    Based of Brown CSCI 1420

    Reads the data from the input file and splits it into normalized inputs 
    and labels. Runs PCA to reduce the feature space.

    :param file_name: path to the desired data file
    :return: two numpy arrays, one containing the inputs and one containing
              the labels
             a fitted pca object
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
        col = inputs[:,j]
        mu = np.mean(col)
        sigma = np.std(col)
        if sigma == 0: sigma = 1
        inputs[:,j] = 1/sigma * (col - mu)

    inputs, labels = read_data(file_name)

    pca = decomposition.PCA(n_components=target_features)
    pca.fit(inputs)
    inputs = pca.transform(inputs)

    return inputs, labels, pca
