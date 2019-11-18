#!/bin/usr/python3

import os
import pandas as pd
import numpy as np
import keras
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


def format_data(data):
    data = data.replace('<p>', '').replace('</p>', '').replace('\n', '').replace('"',"'").replace('\r','')\
    .replace('<li>','').replace('</li>','').replace('<ul>','').replace('</ul>','').replace('<blockquote>','')\
    .replace('</blockquote>','').replace('<a href=','').replace('</a>','').replace("rel='noreferrer'>",'')\
    .replace('</strong>','').replace('<strong>','').replace('<pre>','').replace('</pre>','')\
    .replace('<code>','').replace('</code>','').replace('/r/','')
    
    data = data.strip()
    
    return data


def format_data_read(df):
	QandA = []
	qlen = []
	alen = []

	for ix, row in df.iterrows():
		question = format_data(row['question'].lower())
		answer = format_data(row['answer'].lower())

		question = question.split()
		answer   = answer.split()

		qlen.append(len(question))
		alen.append(len(answer))

		QandA.append([question, answer])
	    
	max_qlen = max(qlen)
	max_answ = max(alen)

	return max_qlen, max_answ, QandA


def vectorize_data(data, word_index, max_quest_len, max_answer_len):
	"""
	Create a function for vectorizing the stories, questions and answers:
	(Basically we are assigning numbers to words)

	"""

	Qlist = [] # vectorized questions
	Alist = [] # vectorized answers
	 
	for question, answer in data:
		q = [word_index[word.lower()] for word in question]
		a = [word_index[word.lower()] for word in answer]

		Qlist.append(q)
		Alist.append(a)

	return pad_sequences(Qlist, maxlen = max_quest_len), pad_sequences(Alist, maxlen = max_answer_len)



def main():
	print("Reading in data...")
	df = pd.read_csv('df_afifth.csv')
	df.drop(columns='Unnamed: 0', inplace = True)
	df.dropna(inplace=True)

	max_qlen, max_answ, train_data = format_data_read(df)
	
	vocab = pd.read_pickle(open('vocab_dict_afifth.pkl', 'rb'))
	vocab_len = len(vocab) + 1


	# # Split data into training and validation
	# percentage = .05 #.20
	# train_val_split = int(df.shape[0] * percentage)

	# dftrain     = df.iloc[train_val_split :]
	# train_data  = QandA[train_val_split :]

	# dfvalid    = df.iloc[:train_val_split]
	# valid_data = QandA[:train_val_split]


	print("Tokenizing vocabulary...")
	#Create an instance of the tokenizer object:
	tokenizer = Tokenizer(filters = [])
	tokenizer.fit_on_texts(vocab)
	print("Finished tokenizing vocabulary.")

	# Tokenizer creates a Dictionary that maps every word in our vocab to an index
	# It has been automatically lowercased
	# This tokenizer can give different indexes for different words depending on when we run it
	word_index = tokenizer.word_index

	print("Vectorizing data...")
	# Tokenize, pad the questions and answers [for both training and validation set]
	questions_train, answers_train = vectorize_data(train_data, word_index, max_qlen, max_answ)
	#questions_valid, answers_valid = vectorize_dataV2(valid_data, word_index,  max_qlen, max_answ)
	print("Finished vectorizing data.")

	print("Encoded input data: {}, with max length of {}. (Questions)".format(questions_train.shape, max_qlen))
	print("Decoded output data: {}, with max length of {}. (Answers)".format(answers_train.shape, max_answ))

	#print("Onehot encoding...")
	# Tokenize, pad the answers, and one hot encode
	#onehot_answers = keras.utils.to_categorical(answers_train, vocab_len)
	#print("Onehot vector: {}".format(onehot_answers.shape))

	# Save processed arrays for training
	print("saving training sets...")
	#np.savez_compressed('questions_reddit', questions_train)
	#np.savez_compressed('answers_reddit', answers_train)
	np.save('questions_reddit.npy', questions_train)
	np.save('answers_reddit.npy', answers_train)
	#np.savez_compressed('onehot_reddit', onehot_answers)

main()