#!/bin/usr/python3
import os
import numpy as np
import pandas as pd
import numpy as np

import keras
import tensorflow as tf

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

def main():
	questions_train = np.load('./questions_reddit.npy')
	answers_train = np.load('./answers_reddit.npy')

	vocab_len = 148764

	# Tokenize, pad the answers, and one hot encode
	print("Tokenizing...")
	onehot_answers = keras.utils.to_categorical(answers_train, vocab_len)
	print("Onehot vector: {}".format(onehot_answers.shape))


	encoder_inputs = tf.keras.layers.Input(shape=( None , ))
	encoder_embedding = tf.keras.layers.Embedding( vocab_len, 100 , mask_zero=True ) (encoder_inputs)
	encoder_outputs , state_h , state_c = tf.keras.layers.LSTM( 100 , return_state=True )( encoder_embedding )
	encoder_states = [ state_h , state_c ]

	decoder_inputs = tf.keras.layers.Input(shape=( None ,  ))
	decoder_embedding = tf.keras.layers.Embedding( vocab_len, 100 , mask_zero=True) (decoder_inputs)
	decoder_lstm = tf.keras.layers.LSTM( 100 , return_state=True , return_sequences=True )
	decoder_outputs , _ , _ = decoder_lstm ( decoder_embedding , initial_state=encoder_states )
	decoder_dense = tf.keras.layers.Dense( vocab_len , activation=tf.keras.activations.softmax ) 
	output = decoder_dense ( decoder_outputs )

	model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output )
	model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='categorical_crossentropy')

	model.summary()

	history = model.fit([questions_train, answers_train], onehot_answers, batch_size=50, epochs = 50)

	print("Saving model...")
	DATADIR = './'
	# Serialize model to JSON
	model_file_name = "model.json"
	MODEL_PATH_NAME = os.path.join(DATADIR, model_file_name)

	model_json = model.to_json()
	with open(MODEL_PATH_NAME, "w") as json_file:
	    json_file.write(model_json)

	# Serialize weights to HDF5
	weights_file_name = "model.h5"
	WEIGHT_PATH_NAME = os.path.join(DATADIR, weights_file_name)
	model.save_weights(WEIGHT_PATH_NAME)
	print("Saved model to disk")	

main()	