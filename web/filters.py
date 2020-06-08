# -*- coding: utf-8 -*-

import json
import os
import math
import Stemmer

BLOCKSIZE = 10

def filter_symbols(word):
    extras = [',','.',':','\'','"','-','¡','¿','#','?','!','(',')','»','«',';']

    for e in extras:
        word = word.replace(e,'')
    return word

def filter_file(file, stopwords):

    stemmer = Stemmer.Stemmer('spanish')

    with open(file) as f:
        tweet = [word.lower() for line in f for word in line.split()]

    #Filtramos los simbolos
    tweet = [filter_symbols(word) for word in tweet]

    #Filtramos los stopwords
    tweet = [word for word in tweet if word not in stopwords]

    return list(stemmer.stemWords(tweet))


def writeBlock(block, id):
    with open("temp"+str(id)+".txt", "w") as mi:
        for tu in block:
            mi.write(str(tu[0]) + ' ' + str(tu[1]) + ' ' + str(tu[2]) + '\n')

def buildTempFiles(tweets):
    size = 0
    block = []
    nblock = 0
    for i in range(len(tweets)):
        tweet_filtrado = filter_file(tweets[i], stopwords)
        tweet_filtrado_unique = list(set(tweet_filtrado))
        for word in tweet_filtrado_unique:
            block.append((word, i, tweet_filtrado.count(word)))
            size += 1
            if (size == BLOCKSIZE):
                writeBlock(sorted(block), nblock)
                size = 0
                block = []
                nblock += 1
    if(len(block)):
        writeBlock(sorted(block), nblock)
        nblock += 1
    return nblock

def combine(id1, id2, outfile):
    with open("temp" + str(id1) + str(id2) + ".txt", "w") as mi:
        with open("temp" + str(id1) + ".txt") as f1, open("temp" + str(id2) + ".txt") as f2:
            l1 = f1.readline()
            l2 = f2.readline()
            while l1 and l2:
                if(l1<l2):
                    mi.write(l1)
                    l1 = f1.readline()
                else:
                    mi.write(l2)
                    l2 = f2.readline()
            while l1:
                mi.write(l1)
                l1 = f1.readline()
            while l2:
                mi.write(l2)
                l2 = f2.readline()
    os.remove("temp" + str(id1) + ".txt")
    os.remove("temp" + str(id2) + ".txt")
    os.rename("temp" + str(id1) + str(id2) + ".txt", "temp" + str(outfile) + ".txt")


def writeIndex(f):
    with open("invertedIndex.txt", "w") as mi:
        with open(f) as f1:
            l1 = f1.readline().split()
            while l1:
                word = l1[0]
                mi.write(word + ' ')
                while l1 and word==l1[0]:
                    mi.write(l1[1] + ' ' + l1[2] + ' ')
                    l1 = f1.readline().split()
                mi.write('\n')
    os.remove("temp0.txt")

def buildIndex(tweets):
    nblock = buildTempFiles(tweets)
    for i in range(math.ceil(math.log2(nblock))):
        for j in range(0,nblock-1,2):
            combine(j,j+1,j//2)
        if(nblock%2):
            os.rename("temp" + str(nblock-1) + ".txt", "temp" + str((nblock-1)//2) + ".txt")
        nblock = math.ceil(nblock/2)
    writeIndex("temp0.txt")

tweets = ['t1.txt','t2.txt','t3.txt','t4.txt']

with open("stopwords.txt") as sw:
        stopwords = json.load(sw)

stopwords = stopwords["words"]

buildIndex(tweets)


