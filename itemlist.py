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

    if login_session['logged_in'] == False:
        return redirect('/welcome')

    redirect(url_for('metalitems'))


@app.route('/welcome')
def welcome():

    return render_template('welcome.html')

#--METALITEMS-------------------------------------------------------------


@app.route('/metalitems')
def metalitems():

    if login_session['logged_in'] == False:
        return redirect('/')

    _user_id = login_session['userid']
    _categories = session.query(Category).filter_by(user_id=_user_id)

    return render_template('metalitems.html', categories=_categories)


@app.route('/login', methods=['POST'])
def login():

    _password = request.form['password']
    _username = request.form['username']

    user = session.query(User).filter_by(username=_username).first()

    if user is not None:
        if check_password_hash(user.password, _password) == True:
            login_session['logged_in'] = True
            login_session['userid'] = user.id
            _flashmessage = 'Hi ' + user.username + ', you did successfully log in.'
            flash(_flashmessage)
        else:
            login_session['logged_in'] = False
            _flashmessage = user.username + ', did you forget your password? Try it again.'
            flash(_flashmessage)

    else:
        _flashmessage = 'User does not exist, seems you need to sign up first.'
        flash(_flashmessage)

    return redirect(url_for('metalitems'))


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


@app.route('/newcategory', methods=['POST'])
def newcategory():

    _categoryname = request.form['newcategory']
    _user_id = login_session['userid']
    newCategory = Category(name=_categoryname, user_id=_user_id)
    session.add(newCategory)
    session.commit()

    return redirect(url_for('metalitems'))

#--NEWITEMS--------------------------------------------------------------------


@app.route('/newitem/<int:categoryid>', methods=['POST', 'GET'])
def newitem(categoryid):
    if request.method == 'POST':
        _itemtitle = request.form['newitemtitle']
        _itemdescription = request.form['newitemdescription']
        _user_id = login_session['userid']
        _newItem = Item(title=_itemtitle, description=_itemdescription,
                        category_id=categoryid, user_id=_user_id)
        session.add(_newItem)
        session.commit()
        return redirect(url_for('metalitems'))
    else:
        return render_template('newmetalitem.html', categoryid=categoryid)

if __name__ == '__main__':
    print app.url_map
    app.secret_key = 'geheim'
    app.debug = True

    app.run(host='0.0.0.0', port=5000)
