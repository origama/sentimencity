#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import nltk
import requests
import feedparser
import cPickle as pickle
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger('default')


class TrainSet:
    '''
    This class handles training sets in the form of array of tuples
    each tuple contains a sentence and a polarity (positive/negative/neutral)
    '''
    training_set=""
    def __init__(self,path=""):
        logger
        self.load(path)

    def load(self,path=""):
        self.training_set=[]
        if path!="":
            try:
                logger.info("loading training set from %s"%path)
                self.training_set = pickle.load( open( path, "rb" ) )
            except:
		logger.error("Couldn't load training set from %s. Training set is set to empty."%path)

    def save(self,path=""):
        if path=="":
            path="noname.pickle"
        pickle.dump( self.training_set, open( path, "wb" ) )

    def put(self,*args):
        if len(args)==1 and isinstance(args[0],tuple):
            self.training_set.append(args[0])
        elif len(args)==2 and isinstance(args[0],string) and isinstance(args[1],string):
            self.training_set.append((args[0],args[1]))
        else:
            raise ValueError("argument have to be a tuple or two strings")

    def get(self):
        return self.training_set

class Trainer:
    '''
    This class creates a training set by reading a text document, tockenizing in sentences and asking a human for the polarity of each sentence
    '''
    trainset=None
    text=[]

    def __init__(self,sourcetype="file",textsource='',trainsetfile=''):
        if sourcetype=="file":
            #reads an example article from disk
            file=codecs.open(textsource, encoding='utf-8', mode='r')
            self.text.append(file.read())
            file.close()
        #if pathtype=="url":
        if sourcetype=="feed":
            feed=ArticleFeed(textsource)
            self.text=feed.getArticles()
        self.trainset=TrainSet(trainsetfile)

    def start(self):
        tokenizer=nltk.data.load('tokenizers/punkt/italian.pickle')
        sentences=[]
        for text in self.text:
            [sentences.append(sentence) for sentence in tokenizer.tokenize(text)]
        logger.info("extracted %d total sentences"%len(sentences))
        for s in sentences:
            print('\n ----------- \n\n')
            polarity=self.pos_or_neg(s)
            if polarity=='pos' or polarity=='neg':
                self.trainset.put((s,polarity))
            if polarity=='quit':
                break

    def save(self,path=""):
        self.trainset.save(path)

    def pos_or_neg(self,sentence):
        while "the polarity is invalid":
            reply = str(raw_input(sentence.encode("utf-8")+' (p/n/i/q): ')).lower().strip()
            if reply[:1] == 'p':
                return "pos"
            if reply[:1] == 'n':
                return "neg"
            if reply[:1] == 'i':
                return "ign"
            if reply[:1] == 'q':
                return "quit"


class ArticleFeed:
    feed=None
    url=""
    def __init__(self,url):
        self.url=url
        self.refresh()

    def refresh(self):
        self.feed=feedparser.parse(self.url)
        logger.info("Loaded %d articles"%len(self.feed['items']))
         
    def getFeedTitle(self):
        return self.feed['feed']['title']

    def getArticles(self):
        articles=[]
        for item in self.feed['items']:
            page=requests.get(item['link'])
            soup=BeautifulSoup(page.content,'html.parser')
            [i.extract() for i in soup('script')] #getting rid of ads
            paragraphs=soup('article')[0]('p')
            article=""
            for p in paragraphs:
                article+=p.text
            logger.debug(article)
            logger.debug("\n\n")
            articles.append(article)
        return articles
            

if __name__ == "__main__":
    tset=TrainSet('training_set.pickle')
    #print(tset.get())
    

    #trainer=Trainer("file",'example1.txt','')
    #trainer.start()
    #print(trainer.trainset.get())
    #trainer.save("pippo")
    
    trainer=Trainer("feed",'http://www.cataniatoday.it/rss','feed.pickle')
    trainer.start()
    print(trainer.trainset.get())
    trainer.save("pippo")

    #computes the frequency of each word in the text
    #fd=nltk.FreqDist(testo.split())
    
    #plots 50 more frequent words
    #fd.plot(50)
    
    #tokenizes the text with standard tokenizer
    #l=sent_tokenize(testo)
    #print(l)
    
    #tokenizes using italian punctuation rules
 
