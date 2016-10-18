# RTC-Document_Summarization
This is the repo for the Document summarization

You will have to install: 

1. BeautifulSoup: `pip install BeautifulSoup`

2. nltk: `pip install nltk`

3. pickle: `pip install pickle`

4. json: `pip install simplejson`

Project:

Step 1: Extracting the knowledge base.

To do this, run all cell in order in create_knowledge_base.ipynb

This picks all the frequently used words in training data catchphrases and puts them in a dictionary (key:value) = (word:frequency). It then pickles this dict into a pickle file which will be used in step 2. 

Step 2: Extracting summary of new doc.

To do this, run :

`python HakunaSummarizer.py <filename> <num_senetences>`

Extarcts summary, and puts dict of (key:value) = (keyword: sentence) into a json file, which is called by index.html in the same script. index.html parses the json file as dendrogram under the hood and displays the results.
