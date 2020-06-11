# -*- coding: utf-8 -*-

import json
import sys
import emoji
import Stemmer

BLOCKSIZE = 1000

Blocks = 0

def filter_symbols(word):
    extras = [',','.',':','\'','"','-','¡','¿','#','?','!','(',')','»','«',';','%','{','}','[',']','$','&','/','=',
              '…','+','-','*','_','^','`','|','°','”','✅','‘','“','⁦','—','⏩','⚠️','✌','➡️','♫','♩','❤','▶','√','🤷‍♀️'
              '🆘']

    for e in extras:
        word = word.replace(e,'')

    return emoji.demojize(word, delimiters=("", ""))

def filter_file(file, stopwords):

    stemmer = Stemmer.Stemmer('spanish')

    tweet = [word.lower() for word in file.split()]

    #Filtramos los simbolos
    tweet = [filter_symbols(word) for word in tweet]

    #Filtramos los websites
    tweet = [word for word in tweet if not word.startswith("http") and not word.startswith("@")
             and len(word)]

    #Filtramos los stopwords
    tweet = [word for word in tweet if word not in stopwords]

    return list(stemmer.stemWords(tweet))


def writeBlock(block, id):
    with open(str(id)+".txt", "w") as mi:
        for tu in block:
            mi.write(str(tu[0]) + ' ' + str(tu[1]) + ' ' + str(tu[2]) + '\n')


def buildBlocks(tweets, stopwords):
    block = []
    nblock = 0
    if Blocks:
        with open(str(Blocks-1) + ".txt") as mi:
            l1 = mi.readline().split()
            block.append({l1[0],int(l1[1]),int(l1[2])})
        nblock = len(block)-1
    for i in range(len(tweets)):
        tweet_filtrado = filter_file(tweets[i].text, stopwords)
        tweet_filtrado_unique = list(set(tweet_filtrado))
        for word in tweet_filtrado_unique:
            block.append((word,tweets[i].id,tweet_filtrado.count(word)))
            if (sys.getsizeof(block) > BLOCKSIZE):
                tmp_block = block[len(block)-1]
                block.pop()
                writeBlock(sorted(block), nblock)
                block = [tmp_block]
                nblock += 1
    if(len(block)):
        writeBlock(sorted(block), nblock)
        nblock += 1
    return nblock


def addTweets(tweets):
    global Blocks
    with open("templates/stopwords.txt") as sw:
        stopwords = json.load(sw)
    stopwords = stopwords["words"]

    Blocks += buildBlocks(tweets,stopwords)
    return Blocks

def initBlocks(tweets):
    global Blocks
    Blocks = 0
    addTweets(tweets)
    return Blocks