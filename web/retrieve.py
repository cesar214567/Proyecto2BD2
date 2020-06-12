# -*- coding: utf-8 -*-

import json
import filters as filters
import collections
import Stemmer
import math
import os

matrix = collections.defaultdict(dict)

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

def combine(id1, id2, query):
    with open(str(id1) + "_" + str(id2) + ".txt", "w") as mi:
        with open(str(id1)) as f1, open(str(id2) + ".txt") as f2:
            l1 = f1.readline()
            l2 = f2.readline()
            while l1 and l2:
                if(l1<l2):
                    if l1.split()[0] in query:
                        mi.write(l1)
                    l1 = f1.readline()
                else:
                    if l2.split()[0] in query:
                        mi.write(l2)
                    l2 = f2.readline()
            while l1:
                if l1.split()[0] in query:
                    mi.write(l1)
                l1 = f1.readline()
            while l2:
                if l2.split()[0] in query:
                    mi.write(l2)
                l2 = f2.readline()
    os.rename(str(id1) + "_" + str(id2) + ".txt", str(id1))


def writeIndex(f):
    tweets = []
    with open(f) as f1:
        l1 = f1.readline().split()
        while l1:
            word = l1[0]
            while l1 and word==l1[0]:
                tweets.append(l1[1])
                matrix[word][l1[1]] = int(l1[2])
                l1 = f1.readline().split()
    os.remove(f)
    return list(set(tweets))


def retrieve(query):
    f = open("temp.txt", "w+")
    f.close()
    print(filters.Blocks)
    for i in range(filters.Blocks):
        combine("temp.txt",i,query)
    return writeIndex("temp.txt")


def cosineScore(query, k):
    unique_keys = list(set(query))
    tweets = retrieve(unique_keys)
    df = {}
    for i in matrix.keys():
        df[i] = len(matrix[i])
    q = {}
    for i in unique_keys:
        if i in df.keys():
            q[i] = math.log10(1+query.count(i))*math.log10(filters.N/df[i])
    for i in matrix.keys():
        for j in matrix[i].keys():
            if i in df.keys() and j in matrix[i].keys():
                matrix[i][j] = math.log10(1+matrix[i][j]) * math.log10(filters.N/df[i])
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
    with open("templates/stopwords.txt") as sw:
        stopwords = json.load(sw)
    stopwords = stopwords["words"]
    tokens = filter_query(query, stopwords)
    results = cosineScore(tokens,k)
    for i in results:
        print(i)
    return results

if __name__ == '__main__':

   query = input()
   executeQuery(query,10)