def get():
	stopwords=[]
	for line in file('stop_words_eng.txt'):
		word=line.strip()
		stopwords.append(word)
	if len(stopwords)!=0:
		print 'All is done!count:'
		print len(stopwords)
		print stopwords
