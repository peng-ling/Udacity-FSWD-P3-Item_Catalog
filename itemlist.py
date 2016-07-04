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
        return redirect('/welcome')

    return render_template('main.html')

@app.route('/welcome')
def welcome():

    return render_template('welcome.html')


@app.route('/metalitems')
def metalitems():

    if 'username' not in login_session:
        return redirect('/')

    return render_template('metalitems.html')


@app.route('/login', methods=['POST'])
def login():

    print request.form['password']
    print request.form['username']

    _password = request.form['password']
    _username = request.form['username']

    user = session.query(User).filter_by(username=_username).first()

    if user is not None:
        if check_password_hash(user.password, _password) == True:
            login_session['logged_in'] = True
            print login_session
            _flashmessage = 'Hi ' + user.username + ', you did successfully log in.'
            flash(_flashmessage)
        else:
            login_session['logged_in'] = False
            _flashmessage = user.username + ', did you forget your password? Try it again.'
            flash(_flashmessage)

    else:
        _flashmessage = 'User does not exist, seems you need to sign up first.'
        flash(_flashmessage)

    return render_template('metalitems.html')


@app.route('/logout', methods=['POST'])
def logout():

    login_session['logged_in'] = False
    flash('You were successfully logged out')

    return render_template('metalitems.html')


@app.route('/createuser', methods=['POST'])
def createuser():
    return render_template('createuser.html')


@app.route('/adduser', methods=['POST'])
def adduser():

    _newpassword = generate_password_hash(request.form['newpassword'])
    _newusername = request.form['newusername']

    _userexists = session.query(User).filter_by(username=_newusername).first()

    if _userexists is not None:
        _flashmessage = 'Unfortunately the username: ' + request.form['newusername'] \
            + ' is already ocupied by someone else, choose an other one!'
        flash(_flashmessage)

        return render_template('createuser.html')

    newUser = User(username=_newusername, password=_newpassword)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(username=_newusername).first()
    _flashmessage = 'Welcome ' + user.username + '! Log in to start.'
    flash(_flashmessage)

    return render_template('metalitems.html')

if __name__ == '__main__':
    print app.url_map
    app.secret_key = 'geheim'
    app.debug = True

    app.run(host='0.0.0.0', port=5000)
