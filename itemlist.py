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

    if 'logged_in' not in login_session:

        print 'NONE'

        return redirect('/welcome')

    else:

        if login_session['logged_in'] == False:
            return redirect('/welcome')

        return redirect(url_for('metalitems'))


@app.route('/welcome')
def welcome():

    return render_template('welcome.html')

#--METALITEMS-------------------------------------------------------------


@app.route('/metalitems')
def metalitems():

    if 'logged_in' not in login_session:

        return redirect('/welcome')

    else:

        if login_session['logged_in'] == False:

            return redirect('/welcome')

        _user_id = login_session['userid']
        _categories = session.query(Category).filter_by(user_id=_user_id)
        _items = session.query(Item).filter_by(user_id=_user_id)

    return render_template('metalitems.html', categories=_categories, items=_items)


@app.route('/login', methods=['POST'])
def login():

    _password = request.form['password']
    _username = request.form['username']

    user = session.query(User).filter_by(username=_username).first()

    print '--------------USER FOUND IN DB-----------------'

    if user is not None:
        if check_password_hash(user.password, _password) == True:
            print '--------------USER PROVIDED CORRECT PW-----------------'
            login_session['logged_in'] = True
            login_session['userid'] = user.id
            print '--------------SESSION COOKIE SET UP-----------------'
            _flashmessage = 'Hi ' + user.username + ', you did successfully log in.'
            flash(_flashmessage)
            print '--------------FLASH MASTER OF THE UNIVERSE-----------------'
            return redirect('metalitems')

        else:

            login_session['logged_in'] = False
            _flashmessage = user.username + ', did you forget your password? Try it again.'
            flash(_flashmessage)

            print '--------------PW WRONG!!!-----------------'

            return redirect('/welcome')

    else:

        print '--------------USER NOT IN DB-----------------'
        _flashmessage = 'User does not exist, seems you need to sign up first.'
        flash(_flashmessage)

        return redirect('/welcome')

    print '--------------WHATS GOING WRONG HERE?-----------------'
    # return redirect(url_for('metalitems'))


@app.route('/logout', methods=['POST'])
def logout():

    login_session['logged_in'] = False
    flash('You were successfully logged out')

    return redirect(url_for('metalitems'))


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


@app.route('/deletecategory/<int:categoryid>', methods=['POST'])
def deletecategory(categoryid):

    if request.method == 'POST':
        _user_id = login_session['userid']
        print _user_id
        print categoryid
        _categoryToDelete = session.query(Category).filter_by(
            id=categoryid, user_id=_user_id).first()

        print '--------------------------'
        print _categoryToDelete
        print '--------------------------'

        session.delete(_categoryToDelete)
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

#--DELETEITEMS------------------------------------------------------------


@app.route('/deleteitem/<int:itemid>', methods=['POST', 'GET'])
def deleteitem(itemid):

    if request.method == 'GET':
        _user_id = login_session['userid']
        _itemToDelete = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()
        print '---------------'
        print _itemToDelete.id
        print '---------------'
        session.delete(_itemToDelete)
        session.commit()

    return redirect(url_for('metalitems'))

#--UPDATEITEMS------------------------------------------------------------


@app.route('/updateitem/<int:itemid>', methods=['POST', 'GET'])
def updateitem(itemid):

    if request.method == 'GET':
        _user_id = login_session['userid']
        _itemToUpdate = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()

        return render_template('updatemetalitem.html', itemToUpdate=_itemToUpdate)

    else:
        session.query(Item).filter_by(id=itemid).update(
            {"title": request.form['newitemtitle'], "description": request.form['newitemdescription']})
        session.commit()

    return redirect(url_for('metalitems'))

if __name__ == '__main__':
    print app.url_map
    app.secret_key = 'geheim'
    #app.debug = True

    app.run(host='0.0.0.0', port=5000)
