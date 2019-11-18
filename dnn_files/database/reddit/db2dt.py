#!/bin/usr/python3

import os
import pandas as pd
import sqlite3

def main():

	timeframe =  '2015-01'

	connection = sqlite3.connect('{}.db'.format(timeframe))
	c = connection.cursor()
	# The limit is the size of chunk that we're going to pull at a time from the database.
	limit = 5000
	# Help us make pulls from database
	last_unix = 0
	# Cur_length will tell us when we are done
	cur_length = limit
	# Show us some debugging information
	counter = 0
	# Tells us when we are done building the test set
	test_done = False


	QandATest = []
	QandATrain = []
	kept_tot = 0

	while cur_length == limit:    

		df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} and parent NOT NULL and score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix,limit),connection)
		last_unix = df.tail(1)['unix'].values[0]
		cur_length = len(df)

		if not test_done:
			for ix, row in df.iterrows():
				question = row['parent']
				answer   = row['comment']
				QandATest.append([question, answer])
			test_done = True

		else:
			for ix, row in df.iterrows():
				question = row['parent']
				answer = row['comment']

				if (len(question) < 50) and (len(answer) < 50):

					QandATrain.append([question, answer])
					kept_tot += 1

		counter += 1
		if counter % 20 == 0:
			print(counter*limit,'rows gone through so far')
			print("Of those we have kept {}".format(kept_tot))
		    
	dftest = pd.DataFrame(QandATest, columns=['question', 'answer'])
	dftrain = pd.DataFrame(QandATrain, columns = ['question', 'answer'])

	# Save into csv file
	dftest.to_csv("dftest_tmp.csv")
	dftrain.to_csv("dftrain_tmp.csv")

main()	