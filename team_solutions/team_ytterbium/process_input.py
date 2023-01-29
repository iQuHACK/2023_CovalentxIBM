import numpy as np
import re
import pickle as pk

word_list = [
    "you",
    "address",
    "all",
    "3d",
    "our",
    "over",
    "remove",
    "internet",
    "order",
    "mail",
    "receive",
    "will",
    "people",
    "report",
    "addresses",
    "free",
    "business",
    "email",
    "you",
    "credit",
    "your",
    "font",
    "000",
    "money",
    "hp",
    "hpl",
    "george",
    "650",
    "lab",
    "labs",
    "telnet",
    "857",
    "data",
    "415",
    "85",
    "technology",
    "1999",
    "parts",
    "pm",
    "direct",
    "cs",
    "meeting",
    "original",
    "project",
    "re",
    "edu",
    "table",
    "conference"
]

char_list = [
    ";",
    "(",
    "[",
    "!",
    "$",
    "#"
]


def read_input(input, pca_filename="data/pca.pkl"):

    # MAPPING TO 57 FEATURE SPACE
    input_words = re.findall(r'[a-zA-Z0-9]+', input.lower())
    print(input_words)
    initial_features = np.zeros(57)
    i = 0
    for word in word_list:
        initial_features[i] = input_words.count(word)
        i += 1
    for char in char_list:
        initial_features[i] = input.count(char)
        i += 1
    seq_cap = np.array(list(map(len, re.findall(r"[A-Z]+", input))))
    if len(seq_cap) == 0:
        return initial_features
    initial_features[i] = np.average(seq_cap)
    initial_features[i + 1] = np.max(seq_cap)
    initial_features[i + 2] = np.sum(seq_cap)

    # MAPPING TO 5 FEATURE SPACE
    with open(pca_filename, "rb") as fd:
        pca = pk.load(fd)

    return pca.transform(initial_features)
