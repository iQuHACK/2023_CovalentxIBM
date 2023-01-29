import numpy as np

def predict(feature):
	'''
	input: 
		feature (nd.array): feature
	return :
		p (int): prediction result, 1 for spam 0 for no
	'''
	s = feature.sum()
	return 1 if s > 50 else 0


def transform(text):
	'''
	input:
		text (str): email body text
	return:
		output (nd.array): feature

	'''
	n = 5
	num = len(text)
	output = np.zeros(n)
	for i in range(5):
		output[i] = num + i 
	return output


if __name__ == '__main__':
    pass