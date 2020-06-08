# -*- coding: utf-8 -*-

import json
import collections
import Stemmer
import math

matrixPath = "invertedIndex.txt"
matrix = collections.defaultdict(dict)
N = 4 # numero de documentos

def filter_symbols(word):
    extras = [',','.',':','\'','"','-','¡','¿','#','?','!','(',')','»','«',';']

    for e in extras:
        word = word.replace(e,'')
    return word

def filter_query(query, stopwords):

    stemmer = Stemmer.Stemmer('spanish')

    #Filtramos los simbolos
    query = query.split()

    #Filtramos los stopwords
    query = [word for word in query if word not in stopwords]

    return list(stemmer.stemWords(query))

def retrieve(query):
    tweets = []
    with open(matrixPath) as f:
        for line in f:
            line = line.split()
            for i in range(1, len(line), 2):
                if line[0] in query:
                    tweets.append(int(line[i]))
                    matrix[line[0]][int(line[i])] = int(line[i+1])
    return list(set(tweets))

def cosineScore(query, k):
    unique_keys = list(set(query))
    tweets = retrieve(unique_keys)
    df = {}
    for i in matrix.keys():
        df[i] = len(matrix[i])
    q = {}
    for i in unique_keys:
        q[i] = math.log10(1+query.count(i))*math.log10(N)
    for i in matrix.keys():
        for j in matrix[i].keys():
            matrix[i][j] = math.log10(1+matrix[i][j]) * math.log10(N/df[i])
    score = []
    qacum = sum(q[i]*q[i] for i in q.keys())
    for i in tweets:
        dotProduct = 0
        dacum = 0
        for j in matrix.keys():
            if j in q.keys() and i in matrix[j].keys():
                dotProduct += matrix[j][i]*q[j]
            if i in matrix[j].keys():
                dacum += matrix[j][i]**2
        if qacum and dacum:
            score.append([float(dotProduct/(qacum*dacum)**0.5),i])
    score.sort(reverse=True)
    if(k<len(score)):
        return score[:k]
    else:
        return score


def executeQuery(query,k):
    tokens = filter_query(query, stopwords)
    results = cosineScore(tokens,k)
    for i in results:
        print(i[1])

if __name__ == '__main__':
    with open("stopwords.txt") as sw:
        stopwords = json.load(sw)
    stopwords = stopwords["words"]

    query = input()
    executeQuery(query,10)