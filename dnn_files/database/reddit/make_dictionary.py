import os
import pandas as pd
import pickle

def format_data(data):
	data = data.replace('<p>', '').replace('</p>', '').replace('\n', '').replace('"',"'").replace('\r','')\
	.replace('<li>','').replace('</li>','').replace('<ul>','').replace('</ul>','').replace('<blockquote>','')\
	.replace('</blockquote>','').replace('<a href=','').replace('</a>','').replace("rel='noreferrer'>",'')\
	.replace('</strong>','').replace('<strong>','').replace('<pre>','').replace('</pre>','')\
	.replace('<code>','').replace('</code>','').replace('/r/','')

	data = data.strip()

	return data

def find_question(title, question):
	if title[-1] == '?':
		return title
	elif question[-1] == '?':
		return question
	else: return question

def define_vocab(data_set):
	vocab = set()
	for ques, answ in data_set:
		vocab = vocab.union(set(ques))
		vocab = vocab.union(set(answ))

	return vocab

def get_maxval(max_qlen, max_answ):
	if max_qlen > max_answ:
		return print("We have a maximumally longer question.")
	elif max_answ > max_qlen:
		return print("We have a maximumally longer answer.")
	else:
		return print("Both are of equal size.")


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
	df = pd.read_csv('dftrain_tmp.csv')
	df.drop(columns='Unnamed: 0', inplace = True)
	df.dropna(inplace=True)

	dfkeep = df.iloc[ : (len(df) // 5) ]

	QandA = []
	qlen = []
	alen = []

	for ix, row in dfkeep.iterrows():
		question = format_data(row['question'].lower())
		answer = format_data(row['answer'].lower())

		question = question.split()
		answer   = answer.split()

		qlen.append(len(question)) # get lenghts
		alen.append(len(answer))

		QandA.append([question, answer])


	max_qlen = max(qlen)
	max_answ = max(alen)
	max_len = {'max qusetion length' + ':' + str(max_qlen), 'max answer legnth :' + str(max_answ)}

	# Define vocabulary
	print("Making vocabulary...")
	vocab = define_vocab(QandA)
	vocab_len = len(vocab) + 1
	print("vocab length: {}".format(vocab_len))
	print("Finished building vocabulary.")


	# save lenght dimension information as dictionary
	flen = open('max_length_afifth.txt','w+')
	flen.write('max length: {} \n'.format(max_len))
	flen.write('maximum question length: {} \n'.format(max_qlen))
	flen.write('maximum answer length:" {} \n'.format(max_answ))
	flen.write('vocab dictionary length: {} \n'.format(vocab_len))
	flen.close()

	# Save pandas dataframe used
	dfkeep.to_csv("df_afifth.csv")


	# save vocabulary dictionary
	print("Saving...")
	f = open('vocab_dict_afifth.pkl','wb')
	pickle.dump(vocab, f)
	f.close()

main()