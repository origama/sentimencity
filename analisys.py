import codecs
import nltk
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#reads an example article from disk
file=codecs.open('example1.txt', encoding='utf-8', mode='r')
testo=file.read()

#computes the frequency of each word in the text
fd=nltk.FreqDist(testo.split())

#plots 50 more frequent words
#fd.plot(50)

#tokenizes the text with standard tokenizer
#l=sent_tokenize(testo)
#print(l)

#tokenizes using italian punctuation rules
tokenizer = nltk.data.load('tokenizers/punkt/italian.pickle')
l=tokenizer.tokenize(testo)

sid = SentimentIntensityAnalyzer()

for s in l :
    ss = sid.polarity_scores(s)
    print("\n\n%s"%s)
    for k in ss:
        print("{0}: {1}, ".format(k, ss[k]))

