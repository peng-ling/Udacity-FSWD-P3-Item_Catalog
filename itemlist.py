from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session as login_session
import random
import string
import json
from flask import make_response
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, session, Category, Item, User

app = Flask(__name__)

APPLICATION_NAME = "Paul's Heavy Metal Item Database"


@app.route('/')
def startpage():

    if 'username' not in login_session:
        return redirect('/')

    return render_template('main.html')


@app.route('/metalitems')
def startpage():

    if 'username' not in login_session:
        return redirect('/')

    return render_template('metalitems.html')


@app.route('/login2', methods=['POST'])
def login():

    print request.form['password']
    print request.form['username']

    _password = request.form['password']
    _username = request.form['username']

    user = session.query(User).filter_by(username=_username).first()

    if user is not None:
        print check_password_hash(user.password, _password)
    else:
        print 'user not found'

    return render_template('metalitems.html')


@app.route('/createuser', methods=['POST'])
def createuser():
    return render_template('createuser.html')


@app.route('/adduser', methods=['POST'])
def adduser():

    print request.form['newpassword']
    print request.form['newusername']

    _newpassword = generate_password_hash(request.form['newpassword'])
    _newusername = request.form['newusername']

    newUser = User(username=_newusername, password=_newpassword)
    print newUser
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(username=_newusername).one()
    print user.id

    return render_template('metalitems.html')


if __name__ == '__main__':
    app.secret_key = 'geheim'
    app.debug = True

    app.run(host='0.0.0.0', port=5000)