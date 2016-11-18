from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session as login_session
import random
import string
import json
from flask import make_response
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, session, Category, Item, User, Seri
# Required for Oauth
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)
app.secret_key = 'geheim'

# Get client id from client_secrect.json for google oauth
CLIENT_ID = json.loads(open('/var/www/html/Udacity-FSWD-P3-Item_Catalog/client_secret.json', 'r').read())[
    'web']['client_id']

# Its about Metal!
APPLICATION_NAME = "Paul's Heavy Metal Item Database"


# GETUSERID
# Check if user is already in User Table.
# Used in gconnect to create a none existing user.
def getUserId(email):
    # check if user with email provided from google is already there  and..
    try:
        user = session.query(User).filter_by(
            email=login_session['email']).one()
    # if so return his user id which is used to show only his stuff.
        return user.id
   # If user is not there return none in this case
   # createUser is invoked to creat him on the fly.
    except:
        return None

#CREATEUSER
# creates a user how log in using google oauth the first time.
def createUser():
    newUser = User(username=login_session[
                   'username'], email=login_session['email'])

    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# ISAUTHORIZED
# checks if user is propperly loged on, used for almost every route.
def isauthorized():

    # prepare flash message used in case user is not loged in
    _flashmessage = 'Unauthorized!'

# Check if key loged_in is available in login_session
    if 'logged_in' not in login_session:
        flash(_flashmessage)
        return False

# Check if user is not loged in.
    elif login_session['logged_in'] == False:
        flash(_flashmessage)
        return False

# Yeah! a authorized user is trying to access his Meatl Items!
    elif login_session['logged_in'] == True:
        return True

# Send the unauthorized user back to start.
    else:
        flash(_flashmessage)
        return False


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
    # Create random state variable which is used for google oauth to avoid
    # cross side attacks.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # Create state key and value in login_session.
    login_session['state'] = state

    return render_template('welcome.html', STATE=state)


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
#LOGOUT
@app.route('/logout', methods=['POST'])
def logout():

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':

        login_session['logged_in'] = False
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        redirect(url_for('welcome'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

    return redirect(url_for('metalitems'))


# NEWCATEGORY
@app.route('/newcategory', methods=['POST'])
def newcategory():

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

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

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

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
# gets invoked once a user deletes a category.


@app.route('/deletecategory/<int:categoryid>', methods=['POST'])
def deletecategory(categoryid):

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

    # Make sure site is only accessible by clicking the button and not by typing
    # url in browser.
    if request.method == 'POST':

        _user_id = login_session['userid']


        _categoryToDelete = session.query(Category).filter_by(
            id=categoryid, user_id=_user_id).first()
        # Check if category to be deleted is in database. And if not, tell the
        # user.
        if _categoryToDelete is None:

                _flashmessage = "Unfortunately you're not authorized to delete \
                this category!"
                flash(_flashmessage)

                return redirect(url_for('metalitems'))
        else:

                # Tell user category has been deleted.
                _flashmessage = 'Category ' + _categoryToDelete.name \
                + ' has been delete!'
                flash(_flashmessage)

                # Do it!
                session.delete(_categoryToDelete)
                session.commit()

                return redirect(url_for('metalitems'))


# NEWITEMS
# user can add new items to a category here
@app.route('/newitem/<int:categoryid>', methods=['POST', 'GET'])
def newitem(categoryid):

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

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
            # Return to main page.
            return redirect(url_for('metalitems'))

    # If request is not post but get go here (comming from main page
    # metalitems).
    else:

        _category = session.query(Category).filter_by(
            id=categoryid).first()
        return render_template('newmetalitem.html', categoryid=categoryid,
                               categoryname=_category.name)


# DELETEITEMS
# go here when a user clicks on delete link for an specific item.
@app.route('/deleteitem/<int:itemid>', methods=['GET'])
def deleteitem(itemid):

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

    if request.method == 'GET':
        _user_id = login_session['userid']


        _itemToDelete = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()

        # Check if item to be deleted is in databes and if not tell the user.
        if _itemToDelete is None:

            _flashmessage = "Unfortunately you're not authorized to delete \
                            this item!"
            flash(_flashmessage)

            return redirect(url_for('metalitems'))

        else:

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

    # Check if user is authorized
    if isauthorized() == False:
        return redirect('/welcome')

    # If request is get go here and show site where one can edit an existing
    # item.
    if request.method == 'GET':
        _user_id = login_session['userid']

        _itemToUpdate = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()
        _categories = session.query(Category).filter_by(user_id=_user_id)

        # Check if item to be updated is in database and if not let the user
        # know.
        if _itemToUpdate is None:

            _flashmessage = "Unfortunately you're not authorized to update \
                                this item!"
            flash(_flashmessage)

            return redirect(url_for('metalitems'))

        else:

            return render_template('updatemetalitem.html',
                    itemToUpdate=_itemToUpdate, categories=_categories)

    # Go here when user has updatet his item und clicks the save button.
    else:
        _user_id = login_session['userid']

        _itemToUpdate = session.query(Item).filter_by(
            id=itemid, user_id=_user_id).first()

        _newcategory = session.query(Category).filter_by(
            name=request.form['chosencategory']).first()

        # Check if item to be updated is in database or new category is in
        # database. If not tell the user.
        if _itemToUpdate is None or _newcategory is None:

            _flashmessage = "Unfortunately you're not authorized to update \
                                this item!"
            flash(_flashmessage)

            return redirect(url_for('metalitems'))

        else:

            session.query(Item).filter_by(id=itemid).update(
                {"title": request.form['newitemtitle'],
                "description": request.form['newitemdescription'],
                "category_id": _newcategory.id})
            session.commit()

                # Let the user know that his item has been updated.
            _flashmessage = 'Item ' + _itemToUpdate.title \
                        + ' has been updated.'
            flash(_flashmessage)

            return redirect(url_for('metalitems'))


# OAUTH LOGIN
# Log in with google
@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Check State Parameter to avoid CSRF attacks
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response
    code = request.data

    try:
        # create flow object
        oauth_flow = flow_from_clientsecrets(
            'client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # get credentials by exchanging (what google send back after user
        # authenticated by gplus account log in vs client secret)
        credentials = oauth_flow.step2_exchange(code)

    # if exchange fails send 401 response
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response
    # in case credential exchange succseeded send get request to google
    # with access token from client_secret.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # if result of sendiung accesstoken is an error send 501
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 501)
        response.headers['Content-Type'] = 'application/json'

        return response

    # if resulst of sending accesstoken results not in an error
    # add accesstoken and gplus id to login_session
    login_session["access_token"] = credentials.access_token
    gplus_id = credentials.id_token['sub']

    # check if what user provided for gplus loogin matches what google send back
    # if not sent 401 response
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            'Tokens user id doesnt match user id.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # check if issued_to from client_secret matches what google send back
    # if not sent 401 response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            'Tokens client id  doesnt match apps.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is not allready looged on
    # IF SO HERE IS A TO DO!
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:

        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # If all previously checks (if) are passed user is authenticated
    # request user information from google and store them in
    # login_session
    login_session['gplus_id'] = gplus_id

    _userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    _params = {'access_token': credentials.access_token, 'alt': 'json'}

    answer = requests.get((_userinfo_url), params=_params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['method'] = 'OAUTH'

    # check if user is already in user table if not create user
    if getUserId(login_session['email']) is None:
        createUser()

    # set login_session to loged in, get user id and send the user to his
    # items.
    login_session['logged_in'] = True

    login_session['userid'] = getUserId(login_session['email'])

    response = make_response(json.dumps(
        'Sucsessfully Loged in'), 200)
    response.headers['Content-Type'] = 'application/json'

    _flashmessage = 'Hi ' + data['name'] \
        + ', you did successfully log in.'
    flash(_flashmessage)

    return response

# SERIALIZE BY categoryid
# Returns data of one category for a user as a nice json
@app.route('/serialize/<int:categoryid>', methods=['GET'])
def serializebycategoryid(categoryid):

    # Check if user is authorized.
    if isauthorized() == False:
        return redirect('/welcome')

# Get items of the user filtered by categoryid.
    _items = session.query(Seri).filter_by(user_id=login_session['userid'], \
    category_id=categoryid)
    session.commit()

# Return them as a json
    return jsonify(Metalitems=[i.serialize for i in _items])

# SERIALIZE BY categoryid and itemid
# Returns data of one category for a user as a nice json
@app.route('/serialize/<int:categoryid>/<int:itemid>', methods=['GET'])
def serializebyitemid(categoryid, itemid):

    # Check if user is authorized.
    if isauthorized() == False:
        return redirect('/welcome')

# Get items of the user filtered by categoryid.
    _items = session.query(Seri).filter_by(user_id=login_session['userid'], \
    category_id=categoryid, item_id=itemid)
    session.commit()

# Return them as a json
    return jsonify(Metalitems=[i.serialize for i in _items])


# MAIN
if __name__ == '__main__':
    print app.url_map
    app.secret_key = 'geheim'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = True

    app.run(host='0.0.0.0', port=5000)
