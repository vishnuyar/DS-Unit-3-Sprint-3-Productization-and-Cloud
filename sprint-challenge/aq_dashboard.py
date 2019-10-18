"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ
from home import *

APP = Flask(__name__)


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {}>'.format(self.datetime,self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    recorddata = sendhomedata()
    try:
        for id,record in enumerate(recorddata):
            newrecord = Record(id=id,datetime=record[0],value=record[1])
            DB.session.add(newrecord)
            DB.session.commit()
        message = 'Data refreshed!'
    except Exception as e:
        message = "Error creating records {}".format(e)
    return render_template('refresh.html', message=message)

@APP.route('/')
def riskycities():
    """Getting potentially risky data."""
    riskydata  = Record.query.filter(Record.value>=10).all()
    riskycities = []
    for i,data in enumerate(riskydata):
        dateandvalue = (i,data.datetime,str(data.value))
        riskycities.append(dateandvalue)
    return render_template('base.html', messages=riskycities)

@APP.route('/live')
def root():
    """Base view."""
    body = sendhomedata()
    return render_template('base.html', messages=body)


    