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


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.User).filter(entities.User.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

##asdsaadsdsa

@app.route('/message', methods = ['GET'])
def get_message():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for message in dbResponse:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/message',methods=['POST'])
def create_message():
    c = json.loads(request.form['values'])
    print(c['user_from'])
    user = entities.Message(
        content=c['content'],
        user_from_id=c['user_from']['username']['id'],
        user_to_id=c['user_to']['username']['id']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/message', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    print(message)
    c =  json.loads(request.form['values'])
    for key in c.keys():
        print(key)
        print(c[key])
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'

@app.route('/message', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


@app.route('/authenticate', methods = ["POST"])
def authenticate():
    time.sleep(3)
    message = json.loads(request.data)
    username = message['username']
    password = message['password']
    #2. look in database
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username == username
            ).filter(entities.User.password == password
            ).one()
        session['logged_user'] = user.id
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


@app.route('/chat/')
def chat():
    return render_template('chat.html')


@app.route('/current', methods = ["GET"])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.id == session['logged_user']
        ).first()
    return Response(json.dumps(
            user,
            cls=connector.AlchemyEncoder),
            mimetype='application/json'
        )

@app.route('/logout', methods = ["GET"])
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/messages',methods=['POST'])
def create_message1():
    c = json.loads(request.data)
    user = entities.Message(
        content=c['content'],
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id'],
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    time.sleep(2)
    return 'Created User'

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


if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


