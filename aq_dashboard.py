"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from latestdata import countrycodata
from openaq import OpenAQ
from home import sendpmdata

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

class CORecord(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    country = DB.Column(DB.String(25))
    city = DB.Column(DB.String(25))
    covalue = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<City {} --- Value {}>'.format(self.city,self.covalue)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    recorddata = sendpmdata()
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
    body = sendpmdata()
    return render_template('base.html', messages=body)

@APP.route('/country/<countryname>')
def latestdata(countryname):
    """country Carbon Monoxide data by City"""
    codata = countrycodata(countryname)
    try:
        for id,record in enumerate(codata):
            newrecord = CORecord(id=id,country=countryname,city=record[0],covalue=record[1])
            
            
            DB.session.add(newrecord)
            DB.session.commit()
        message = 'Cities Level added for {}'.format(countryname)
    except Exception as e:
        message = "Error creating records {}".format(e)
    return render_template('corefresh.html', message=message)

@APP.route('/colevels')
def cocities():
    """Getting cities with co risky data."""
    riskydata  = CORecord.query.filter(CORecord.covalue>0).all()
    riskycities = []
    for data in riskydata:
        citycodata = (data.country,data.city,str(data.covalue))
        riskycities.append(citycodata)
    return render_template('country.html', messages=riskycities)

    



    