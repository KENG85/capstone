from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy import func
from flask import Flask, jsonify

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True  


    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kateengard3666980!@localhost:5432/load_scores'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dekcuboaomhapq:a92719d4e48a83565774ead93996355ddbd6aadd2169f0a8b66d39e38aafe56d@ec2-34-225-162-157.compute-1.amazonaws.com:5432/d9eelsnjmt7jvt'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'load_score'
    
    timestamp = db.Column(db.String(30))
    org = db.Column(db.String(30))
    sport = db.Column(db.String(30))
    pos = db.Column(db.String(30))
    player = db.Column(db.String(12), primary_key=True)
    #jump_score = db.Column(db.Numeric)
    sleep = db.Column(db.Integer)
    nutrition = db.Column(db.Integer)
    fatigue = db.Column(db.Integer)
    motivation = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    RPE = db.Column(db.Integer)
    #plus = db.Column(db.Numeric)
    #value = db.Column(db.Numeric)
    tweet = db.Column(db.Text())

    def __init__(self, timestamp, org, sport, pos, player, sleep, nutrition, fatigue, motivation, stress, RPE, tweet):
        
        self.timestamp = timestamp
        self.org = org
        self.sport = sport
        self.pos = pos
        self.player = player
        #self.jump_score = jump_score
        self.sleep = sleep
        self.nutrition = nutrition
        self.fatigue = fatigue
        self.motivation = motivation
        self.stress = stress
        self.RPE = RPE
        #self.plus = plus
        #self.value = value
        self.tweet = tweet

    #load_score = Base.classes.load_score

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        timestamp = request.form['timestamp']
        player = request.form['player']
        #jump_score = request.form['jump_score']
        sport = request.form['sport']
        org = request.form['org']
        pos = request.form['position']
        nutrition = request.form['nutrition']
        sleep = request.form['sleep']
        motivation = request.form['motivation']
        fatigue = request.form['fatigue']
        stress = request.form['stress']
        RPE = request.form['RPE']
        tweet = request.form['sentiment_tweet']

        # print(customer, dealer, rating, comments)
        if player == '' or timestamp == '':
            return render_template('index.html', message='Please enter required fields')

         
        data = Feedback(timestamp=timestamp, org=org, sport=sport, pos=pos, player=player, sleep=sleep, nutrition=nutrition, fatigue=fatigue, motivation=motivation, stress=stress, RPE=RPE, tweet=tweet)
        db.session.add(data)
        db.session.commit()
            #send_mail(player, org, nutrition, sleep, motivation, fatigue, stress, RPE, tweet)    
            
        return render_template('index.html', message='success' )
    return render_template('index.html', message='form submitted')
        
@app.route("/api/red-flags")
def RedFlags():
    #last_week = dt.date(db.timestamp) - dt.timedelta(days=7)
    sel = [Feedback.timestamp, Feedback.player, Feedback.nutrition, Feedback.sleep, Feedback.motivation, Feedback.fatigue, Feedback.stress, Feedback.RPE]
    #plus = [func.avg(Feedback.nutrition, Feedback.sleep, Feedback.motivation) < 8]
    
    #minus = [func.avg(Feedback.fatigue, Feedback.stress, Feedback.RPE) > 5]
    #score = [func.diff(plus - minus)
    results = db.session.query(*sel).filter(Feedback.fatigue and Feedback.stress >=5).filter(Feedback.RPE > 7).all()
    #.filter(Feedback.nutrition <= 8 and Feedback.sleep <= 8).all()
    #results = db.session.query(load_score.fatigue >=4) 
        #filter(db.timestamp > last_week).all()
    #flags = list(np.ravel(results))

    return jsonify(results)


if __name__ == '__main__':
    app.run()
