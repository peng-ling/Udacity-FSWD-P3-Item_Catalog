from flask import Flask, render_template, url_for, request, redirect, flash
#from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session as login_session
import random
import string
#import json
from flask import make_response
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, session, Category, Item, User

app = Flask(__name__)

APPLICATION_NAME = "Paul's Heavy Metal Item Database"

# ROOT
# Routs a user either to the welcomepage in case he is not lohgged in or
# to the Items main page in case he is.


@app.route('/')
def startpage():

    if 'logged_in' not in login_session:
        return redirect('/welcome')
    else:
        if login_session['logged_in'] == False:
            return redirect('/welcome')
        return redirect(url_for('metalitems'))

# WELCOME
# Startpage for a user not logged in.


@app.route('/welcome')
def welcome():

    return render_template('welcome.html')

# METALITEMS
# Main page showing all categories and items of a loged in username.
# A loged in user can view, create, delete and update items and categories
# here.


@app.route('/metalitems')
def metalitems():
    # Check if user is looged in, otherwiese redirect to welcome page.
    if 'logged_in' not in login_session:

        return redirect('/welcome')

    else:
        # Check for user with loginsession, who had logged out and redirect to welcome
        # page.
        if login_session['logged_in'] == False:

            return redirect('/welcome')
# query categories and items of looged in user and render metal items.
        _user_id = login_session['userid']
        _categories = session.query(Category).filter_by(user_id=_user_id)
        _items = session.query(Item).filter_by(user_id=_user_id)

    return render_template('metalitems.html', categories=_categories,
                           items=_items)
# LOGIN


@app.route('/login', methods=['POST'])
def login():
    # once user clicks on login button get username and password.
    _password = request.form['password']
    _username = request.form['username']

# verfiy if user is in user table
    user = session.query(User).filter_by(username=_username).first()

    if user is not None:
        # Check if password provided by the user is correct
        if check_password_hash(user.password, _password) == True:
            # If user logged in successfully set session cookie accordingly.
            login_session['logged_in'] = True
            login_session['userid'] = user.id
# Welcome the user
            _flashmessage = 'Hi ' + user.username \
                + ', you did successfully log in.'
            flash(_flashmessage)
# Redirect to main page where user can see and edit his items / categories.
            return redirect('metalitems')
# In case User provided wrong password, tell him so and redirect to welcome
# page.
        else:

            login_session['logged_in'] = False
            _flashmessage = user.username \
                + ', did you forget your password? Try it again.'
            flash(_flashmessage)

            return redirect('/welcome')

    else:

        # In case user is not in user table, tell him so and redirect to
        # welcome page.
        _flashmessage = 'User does not exist, seems you need to sign up first.'
        flash(_flashmessage)

        return redirect('/welcome')
# LOGOUT
# In case user clicks on logout button, wave godby.


@app.route('/logout', methods=['POST'])
def logout():

    login_session['logged_in'] = False
    flash('You were successfully logged out')

    return redirect(url_for('metalitems'))

# SIGNUP
# Once a new user clicks on signup, redirect to the create user page.


@app.route('/createuser', methods=['POST'])
def createuser():
    return render_template('createuser.html')

# ADDUSER
# Invoked once a user clicks on create account button


@app.route('/adduser', methods=['POST'])
def adduser():

    # get password from request and apply encryption
    _newpassword = generate_password_hash(request.form['newpassword'])
# get username from request.
    _newusername = request.form['newusername']
# querry for username in table users.
    _userexists = session.query(User).filter_by(username=_newusername).first()
# check if username is allready in use and notify if so.
    if _userexists is not None:
        _flashmessage = 'Unfortunately the username: ' \
            + request.form['newusername'] \
            + ' is already ocupied by someone else, choose an other one!'
        flash(_flashmessage)
# In case username is allready occupied, send user back to create user page.
        return render_template('createuser.html')
# If username is not occupied, write new user to table users, and welcome
# him or her.
    newUser = User(username=_newusername, password=_newpassword)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(username=_newusername).first()
    _flashmessage = 'Welcome ' + user.username + '! Log in to start.'
    flash(_flashmessage)

    return render_template('welcome.html')

# NEWCATEGORY


@app.route('/newcategory', methods=['POST'])
def newcategory():
    # Get name of new category from request and check if its not an empty
    # string.
    _categoryname = request.form['newcategory']
# Let user know he is trying to create a no name categroy and redirect to
# item main page.
    if _categoryname == '':
        _flashmessage = 'Name of Category must not be empty!'
        flash(_flashmessage)
        return redirect(url_for('metalitems'))
    _user_id = login_session['userid']
# In case category is valid write it to table category.
    newCategory = Category(name=_categoryname, user_id=_user_id)
    session.add(newCategory)
    session.commit()
# Tell the user his category has been created
    _flashmessage = 'Category ' + _categoryname + ' has been created!'
    flash(_flashmessage)

    return redirect(url_for('metalitems'))

# UPDATE Category
# Here a user can update the name of an already existing category.


@app.route('/updatecategory/<int:categoryid>', methods=['GET', 'POST'])
def updatecategory(categoryid):

    # Go here in case user clicks on update categroy button on metal items
    # page.
    if request.method == 'GET':
        # Get userid for query of category user whants to update
        _user_id = login_session['userid']
# Qurey for category to update.
        _categoryToUpdate = session.query(Category).filter_by(
            id=categoryid, user_id=_user_id).first()
# render template for editing ategory name
        return render_template('updatecategory.html',
                               categoryToUpdate=_categoryToUpdate)
# In case user clicks button update category on update category site go here.
    else:
        # Check if category name is not an empty string
        if request.form['newcategoryname'] == '':
            # If so tell user
            _flashmessage = 'Name of category must not be empty!'
            flash(_flashmessage)

        else:
            # In case propper category name is submitted, update category table
            # with it.
            session.query(Category).filter_by(id=categoryid).update(
                {"name": request.form['newcategoryname']})
            session.commit()
# Tell user category has been updated.
            _flashmessage = 'Name of category has been changed to: ' + \
                request.form['newcategoryname']
            flash(_flashmessage)
# Go back to main page.
        return redirect(url_for('metalitems'))

# DELETE CATEGORY


@app.route('/deletecategory/<int:categoryid>', methods=['POST'])
def deletecategory(categoryid):
    # Make sure site is only accessible by clicking the button and not by typing
    # url in browser.
    if request.method == 'POST':
        _user_id = login_session['userid']
        _categoryToDelete = session.query(Category).filter_by(
            id=categoryid, user_id=_user_id).first()
# Tell user category has been deleted.
        _flashmessage = 'Category ' + _categoryToDelete.name \
            + ' has been delete!'
# Do it!
        session.delete(_categoryToDelete)
        session.commit()

    return redirect(url_for('metalitems'))

# NEWITEMS
# user can add new items to a category here


@app.route('/newitem/<int:categoryid>', methods=['POST', 'GET'])
def newitem(categoryid):
    # If user clicks button add item, check if item title is not an ampty
    # string. Then store the new item in table items.
    if request.method == 'POST':
        _itemtitle = request.form['newitemtitle']
        if _itemtitle == '':
            _flashmessage = 'Name of item must not be empty!'
            flash(_flashmessage)
            return render_template('newmetalitem.html', categoryid=categoryid)
        else:
            _itemdescription = request.form['newitemdescription']
            _user_id = login_session['userid']
            _newItem = Item(title=_itemtitle, description=_itemdescription,
                            category_id=categoryid, user_id=_user_id)
            session.add(_newItem)
            session.commit()
# Let the user know his new item has been safed.
            _flashmessage = 'Item ' + _itemtitle + ' has been created.'
            flash(_flashmessage)
# Return to main page
            return redirect(url_for('metalitems'))
# If request is not post but get go here (comming from main page metalitems)
    else:
        _category = session.query(Category).filter_by(
            id=categoryid).first()
        return render_template('newmetalitem.html', categoryid=categoryid,
                               categoryname=_category.name)

# DELETEITEMS
# go here when a user clicks on delete link for an specific item.


@app.route('/deleteitem/<int:itemid>', methods=['POST', 'GET'])
def deleteitem(itemid):

    if request.method == 'GET':
        _user_id = login_session['userid']
        _itemToDelete = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()

        session.delete(_itemToDelete)
        session.commit()
# Let the user know that his item has been deleted.
        _flashmessage = 'Item ' + _itemToDelete.title \
            + ' has been deleted.'
        flash(_flashmessage)
# return to main page
    return redirect(url_for('metalitems'))

# UPDATEITEMS
# Go here in case a user whants to update an existing item.

@app.route('/updateitem/<int:itemid>', methods=['POST', 'GET'])
def updateitem(itemid):
# If request is get go here and show site where one can edit an existing item.
    if request.method == 'GET':
        _user_id = login_session['userid']
        _itemToUpdate = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()

        return render_template('updatemetalitem.html',
                               itemToUpdate=_itemToUpdate)
# Go here when user has updatet his item und clicks the save button.
    else:
        _user_id = login_session['userid']
        _itemToUpdate = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()

        session.query(Item).filter_by(id=itemid).update(
            {"title": request.form['newitemtitle'],
             "description": request.form['newitemdescription']})
        session.commit()
# Let the user know that his item has been updated.
        _flashmessage = 'Item ' + _itemToUpdate.title \
                        + ' has been updated.'
        flash(_flashmessage)

    return redirect(url_for('metalitems'))

if __name__ == '__main__':
    print app.url_map
    app.secret_key = 'geheim'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = True

    app.run(host='0.0.0.0', port=5000)
