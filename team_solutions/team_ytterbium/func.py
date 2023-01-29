import numpy as np


def transform(text):
	n = 5
	num = len(text)
	output = np.zeros(n)
	for i in range(5):
		output[i] = num + i 
	return output


if __name__ == '__main__':
    pass