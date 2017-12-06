import csv
import pickle
from nltk.corpus import stopwords
import re
from collections import defaultdict
import random
import numpy as np
import pandas as pd

random.seed(2017)

reviewSummaryVectors = {}

# http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}

stopWords = set(stopwords.words("english"))

def loadConceptNetEmbeds():
	embeddings = {}
	with open('numberbatch-17.06.txt', 'rb') as file:
		for line in file:
			line = line.decode("UTF-8")
			embed = line.split(' ')
			embeddings[embed[0]] = embed[1:]
	return embeddings

def cleanReview(review):
	reviewWords = review.lower().split()
	cleanReviewWords = []
	for word in reviewWords:
		if word not in stopWords:
			if word in contractions:
				cleanReviewWords.append(contractions[word])
			else:
				cleanReviewWords.append(word)
	text = " ".join(cleanReviewWords)
	text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	text = re.sub(r'\<a href', ' ', text)
	text = re.sub(r'&amp;', '', text) 
	text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
	text = re.sub(r'<br />', ' ', text)
	text = re.sub(r'\'', ' ', text)
	return text

def cleanSummary(summary):
	summaryWords = summary.lower().split()
	cleanSummaryWords = []
	for word in summaryWords:
		if word in contractions:
			cleanSummaryWords.append(contractions[word])
		else:
			cleanSummaryWords.append(word)
	text = " ".join(cleanSummaryWords)
	text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	text = re.sub(r'\<a href', ' ', text)
	text = re.sub(r'&amp;', '', text) 
	text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
	text = re.sub(r'<br />', ' ', text)
	text = re.sub(r'\'', ' ', text)
	return text

def wordCount(wordCountDictionary,text):
	for w in s.split():
		if w in wordCountDictionary:
			wordCountDictionary[w] += 1
		else:
			wordCountDictionary[w] = 1
	return wordCountDictionary

def convertTextToInt(text, vocabIndex, eos = False):
	ints = []
	for word in text.split():
		if word in vocabIndex:
			ints.append(vocabIndex[word])
		else ints.append(vocabIndex["<UNK>"])
	if eos:
		ints.append(vocabIndex["<EOS>"])
	return ints
def countUnique(text, vocab_index):
	unk = 0
	for word in text.split():
		if word == vocab_index['<UNK>']:
			unk += 1
	return unk

with open('Reviews.csv','rb') as csvfile:
	reviews = csv.reader(csvfile,delimiter=',',quotechar='|')
	print "amazon dataset is loaded!!"
	next(reviews)
	wordCountDictionary = defaultdict(float)
	for row in reviews:
		review,summary = row[9],row[8]
		if len(review)>0 and len(summary)>0:
			wordCountDictionary = wordCount(wordCountDictionary,cleanSummary(summary))
			wordCountDictionary = wordCount(wordCountDictionary,cleanReview(review))
	print "size of amazon food review vocabulary: ",len(wordCountDictionary)
	ConceptNetEmbed = loadConceptNetEmbeds()

	threshold = 15
	vocab_index = {}
	index = 0

	for word in wordCountDictionary.keys():
		if wordCountDictionary[word] >= threshold or word in ConceptNetEmbed:
			vocab_index[word] = index
			index += 1
	symbols = ["<UNK>", "<PAD>", "<EOS>", "<GO>"]
	for s in symbols:
		vocab_index[s] = len(vocab_index)
	index_vocab = {}

	for word in vocab_index.keys():
		index_vocab[vocab_index[word]] = word

	CNDim = 300
	finalWordCount = len(vocab_index)
	embeddings_matrix = np.zeros((finalWordCount, CNDim))
	for word in vocab_index.keys():
		if word in ConceptNetEmbed:
			embeddings_matrix[vocab_index[word]] = ConceptNetEmbed[word]
		else:
			embeddings_matrix[vocab_index[word]] = np.random.uniform(-1.0, 1.0, CNDim)
			ConceptNetEmbed[word] = embeddings_matrix[vocab_index[word]]

	intSummaries = []
	intReviews = []
	lengthSummaries = []
	lenghtReviews = []
	for row in reviews:
		review,summary = row[9],row[8]
		intSummaries.append(convertTextToInt(cleanSummary(summary), vocabIndex))
		intReviews.append(convertTextToInt(cleanReview(review), vocabIndex, eos = True))
		lengthSummaries.append(len(summary))
		lenghtReviews.append(len(review))

	maxReviewLength = 85
	maxSummaryLength = 13

	prunedSummaries = []
	prunedReviews = []

	for length in range(min(lenghtReviews), maxReviewLength):
		for i range(len(intSummaries)):
			if(len(intSummaries[i])>2 and len(intReviews[i])>2 and len(intSummaries[i]) <= maxSummaryLength and countUnique(intSummaries[i], vocab_index)==0 and countUnique(intReviews[i], vocab_index)<=1 and length==len(intReviews[i])):
				prunedReviews.append(intReviews[i])
				prunedSummaries.append(intSummaries[i])
print 'reviews length: ', len(prunedReviews)
print 'summaries length: ', len(prunedSummaries)
import pickle
pickle.dump(prunedReviews, open("prunedReviews.p", "wb"))
pickle.dump(prunedSummaries, open("prunedSummaries.p", "wb"))
