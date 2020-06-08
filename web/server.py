from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import down_tweets as tweetg
import json
import time
db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/queries')
def queries():
    return render_template('queries.html')

@app.route('/query',methods=['POST'])
def query():
    c = json.loads(request.data)
    r_tweet = tweetg.get_tweet_by_id(c['ID'])
    tweet_json =  {}
    tweet_json['ID'] = r_tweet.id
    tweet_json['text'] = r_tweet.text
    tweet_json['date'] = str(r_tweet.created_at)
    tweet_json['lang'] = r_tweet.lang
    list_tweets = []
    list_tweets.append(tweet_json)
    return Response(json.dumps(
            list_tweets),
            mimetype='application/json'
        )

@app.route('/busqueda',methods=['POST'])
def busqueda():
    c = json.loads(request.data)
    query = c["query"]
    #result = get_twets_with_query(query)
    list_tweets = []
    #for id in result:
        #tweet = tweetg.get_tweet_by_id(id)
        #tweet_json =  {}
        #tweet_json['ID'] = r_tweet.id
        #tweet_json['text'] = r_tweet.text
        #tweet_json['date'] = str(r_tweet.created_at)
        #tweet_json['lang'] = r_tweet.lang
        #list_tweets.append(tweet_json)
    
    return Response(json.dumps(
            list_tweets),
            mimetype='application/json'
        )
@app.route('/create',methods=['POST'])
def create():
    c = json.loads(request.data)
    tema = c["tema"]
    tweets = tweetg.get_tweets(tema)
    #create_index(tweets)
    res = {}
    res["status"] = 200
    return Response(json.dumps(
        res), mimetype ='application/json'
    )

if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


