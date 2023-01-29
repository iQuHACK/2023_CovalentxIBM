import sys
import csv
import nltk

word_freq = {}

def extract_features(sample):
	sample_words = set(sample)
	features = {}
	for word in word_list:
		features['contains(%s)' % word] = (word in sample_words)
	return features

with open(sys.argv[1]) as f:
	csv_reader = csv.reader(f, delimiter=';')
	samples = []
	s = 0
	for row in csv_reader:
		s += 1
		# if s >= 1000 and s <= 1599000:
		# 	continue
		words = row[1].split()
		samples.append((words, row[0]))
		for word in words:
			if word in word_freq:
				word_freq[word] += 1
			else:
				word_freq[word] = 1
	word_list = sorted(word_freq)
	training_set = nltk.classify.apply_features(extract_features, samples)
	#print(training_set)
	print(training_set)
	print("*")
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	print(classifier.show_most_informative_features(32))

	tweet = 'I love larry'
	print(classifier.classify(extract_features(tweet.split())))
