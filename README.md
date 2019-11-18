# chat_bot
<img src="./imgs/Neurons-Network_T.jpg">
<p align ="center">
	<h3>ChatBot with Q. and A.'s From Reddit</h3>
</p>
<img src="./imgs/Neurons-Network_B.jpg">

<h2><a name="about">About</a></h2>  
Chatbot is trained on upvoted answers and their associated parent (original question) from Reddit. The user
interface is developed using Python’s Kivy library.

* Workflow completed thus far: downloaded data, pre-processed data, built model, and trained a few models.
* Currently working on training on a larger data set...will need GPU or AWS to do this likely.
* Next steps: limit the vocabulary to allow the LSTM to learn with smaller dataset, finish Kivy GUI, combine
GUI with machine learning model in background.


<h2>Table of Contents</h2>  

* [Dependencies](#dependencies)  
* [How to Use](#how)  
* [Links](#links)   



<h2><a name="dependencies">Dependencies:</a></h2>  
All scripts are written in Python3. The following libraries (and their version) were also used:  

* NumPy 1.15.3  
* ObsPy 1.1.0  
* Pandas 0.23.0  
* Keras (on top of TensorFlow)  2.2.4  
* TensorFlow 1.8.0  
* Matplotlib
* sqlite3
* bz2
* kivy


<h2><a name="how">How to Use</a></h2>  
Coming Soon.  


<h2><a name="links">DataSet</a></h2>
* Torrent file of one month of Reddit data can be found <a href= 'https://mega.nz/#!ysBWXRqK!yPXLr25PgJi184pbJU3GtnqUY4wG7YvuPpxJjEmnb9A'>here</a>.


