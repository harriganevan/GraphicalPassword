from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
import db as database
import re #for regex
import random
from flask_mail import Mail
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

views = Blueprint('views', __name__)

#regex used to check if an email is a valid format
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

@views.route('/')
def home_redirect():
    return redirect('/home')

@views.route("/home")
def home():
    session.clear()
    return render_template("homepage.html")

@views.route("/login1", methods=('GET', 'POST'))
def login1():
    session.clear()
    if request.method == 'POST':
        email = request.form['email'] #get email from form

        error = None

        #check if email exists
        db = database.get_db()
        usernamecheck = db.execute('SELECT COUNT(*) FROM user WHERE username = ?', (email,)).fetchone()
        if (usernamecheck[0] == 0):
            error = "username doesn't exists"

        #checking if email is valid
        if(not re.fullmatch(regex, email)): 
            error = "not valid email"

        if error is None:
            session['username'] = email #session so that email can be accessed on login2
            return redirect(url_for('views.login2'))

        flash(error) #display errors on current page
        
    return render_template("login1.html")

@views.route("/login2", methods=('GET', 'POST'))
def login2():
    #if user tried to skip login1
    if session.get('username') is None:
        return redirect(url_for('views.home'))
    
    user = session.get('username')
    
    db = database.get_db() #create database connection

    #get users images
    getimages = db.execute('SELECT images FROM user WHERE username = ?', (user,)).fetchone()
    images = getimages[0]

    images = str(images)

    #store users images ids in a list
    imgIDList = []
    for i in range(0,18,2):
        temp = images[i:i+2]
        imgIDList.append(int(temp))

    #store users images srcs in a list
    imgSrcList = []
    for i in range(9):
        src = db.execute('SELECT src FROM images WHERE id = ?', (imgIDList[i],)).fetchone()
        imgSrcList.append(src[0])

    #randomize the images, keeping same index pairs
    zipped = list(zip(imgIDList, imgSrcList))
    random.shuffle(zipped)
    imgIDList, imgSrcList = zip(*zipped)

    #check if account is locked
    locksquery = db.execute('SELECT locked FROM user WHERE username = ?', (user,)).fetchone()
    if(locksquery[0] == 1):
        flash('account locked')
        return redirect(url_for('views.forgot'))

    if request.method == 'POST':
        password = request.form['password']

        error = None

        #get users current remaining attempts
        attemptsquery = db.execute('SELECT attempts FROM user WHERE username = ?', (user,)).fetchone()
        attempts = attemptsquery[0]
        
        #check if password is correct
        pwcheck = db.execute('SELECT pw FROM user WHERE username = ?', (user,)).fetchone()
        if(not check_password_hash(pwcheck[0], password)):
            error = "incorrect password"
            attempts = attempts-1
            db.execute('UPDATE user SET attempts = ? WHERE username = ?', (attempts, user,))
            db.commit()

        #if user is out of attempts - lock account
        if(attempts == 0):
            db.execute('UPDATE user SET locked = 1 WHERE username = ?', (user,))
            db.commit()
            flash('account locked')
            return redirect(url_for('views.forgot'))

        #if password is correct
        if error is None:
            session['password'] = password #set for target
            return redirect(url_for('views.target'))
        
        flash(error + ': ' + str(attempts) + ' attempts left')

    return render_template("login2.html", imgIDList=imgIDList, imgSrcList=imgSrcList)

@views.route("/signup1", methods=('GET', 'POST'))
def signup1():
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        fname = request.form['firstname']
        lname = request.form['lastname']

        error = None

        #check if email exists
        db = database.get_db()
        usernamecheck = db.execute('SELECT COUNT(*) FROM user WHERE username = ?', (email,)).fetchone()
        if (usernamecheck[0] != 0):
            error = "username already exists"

        if (not re.fullmatch(regex, email)):
            error = "not valid email"
        elif not fname:
            error = 'first name is required'
        elif not lname:
            error = 'last name is required'

        if error is None:
            session['username'] = email
            session['fname'] = fname
            session['lname'] = lname
            return redirect(url_for("views.signup2"))
        
        flash(error)

    return render_template("signup1.html")

@views.route("/signup2", methods=('GET', 'POST'))
def signup2():
    #if user tried to skip signup1 or has already been logged in
    if session.get('username') is None:
        return redirect(url_for('views.home'))
    if session.get('target') is not None:
        return redirect(url_for('views.target'))
    
    if request.method == 'POST':
        password = request.form['password']

        session['password'] = password

        return redirect(url_for('views.signup3'))
    
    #generate random image IDs
    imgIDList = []
    while(len(imgIDList) < 9):
        rand = random.randint(10,36) #make sure no duplicates
        if rand not in imgIDList:
            imgIDList.append(rand)

    db = database.get_db()

    #use random image IDs and get their src value
    imgSrcList = []
    for i in range(9):
        src = db.execute('SELECT src FROM images WHERE id = ?', (imgIDList[i],)).fetchone()
        imgSrcList.append(src[0])

    session['imgIDs'] = imgIDList #so we can access their ids and store them on signup3
    session['imgSrc'] = imgSrcList

    return render_template("signup2.html", imgIDList=imgIDList, imgSrcList=imgSrcList)

@views.route("/signup3", methods=('GET', 'POST'))
def signup3():
    #if user has tried to skip signup1 or signup2 or is already logged in
    if session.get('username') is None:
        return redirect(url_for('views.home'))
    if session.get('password') is None:
        return redirect(url_for('views.signup2'))
    if session.get('target') is not None:
        return redirect(url_for('views.target'))
    
    user = session.get('username')
    fname = session.get('fname')
    lname = session.get('lname')
    password = session.get('password')

    imgIDList = session.get('imgIDs')
    imgSrcList = session.get('imgSrc')

    #shuffle ids and srcs, keeping matching indexes
    zipped = list(zip(imgIDList, imgSrcList))
    random.shuffle(zipped)
    imgIDList, imgSrcList = zip(*zipped)

    if request.method == 'POST':
        allIDs = "" #will store a concatenated version of users images ids
        for i in range(len(imgIDList)): 
            allIDs = allIDs + str(imgIDList[i])

        second_password = request.form['password']
        if (int(password) == int(second_password)): #if passwords match
            db = database.get_db()
            if session.get('reset') is not None:
                db.execute('UPDATE user SET pw = ?, images = ?, attempts = ?, locked = ? WHERE username = ?', (generate_password_hash(password), allIDs, 4, 0, user))
                db.commit()
                return redirect(url_for('views.target'))
            else:
                db.execute('INSERT INTO user (username, fname, lname, pw, attempts, locked, images) VALUES (?, ?, ?, ?, 4, 0, ?)', (user, fname, lname, generate_password_hash(password), allIDs))
                db.commit()
                return redirect(url_for('views.target'))
        else:
            session.pop('password')
            flash('password confirmation wrong - retry')
            return redirect(url_for('views.signup2'))

    return render_template("signup3.html", imgIDList=imgIDList, imgSrcList=imgSrcList)

@views.route("/forgot", methods=('GET', 'POST'))
def forgot():

    session.clear()

    mail = Mail(current_app)

    if request.method == 'POST':
        email = request.form['email']

        msg = Message("Password Reset for Graphical Passwords", sender="graphicalpws@gmail.com", recipients=[email])
        
        db = database.get_db()

        id = db.execute('SELECT id FROM user WHERE username = ?', (email,)).fetchone()
        
        encID = fernet.encrypt(str(id[0]).encode())
        encID = str(encID)
        sendEnc = encID[2:len(encID)-1]

        msg.body = """
        Click the link to reset your password
        http://127.0.0.1:5000/reset/{}""".format(sendEnc)
        mail.send(msg)

    return render_template("forgot.html")

@views.route("/target")
def target():
    #if user is not logged in
    if session.get('username') is None:
        return redirect(url_for('views.home'))
    if session.get('password') is None:
        return redirect(url_for('views.signup2'))
    session['target'] = 'set' #user has reached the target page and is logged in - cannot go back to signup2 or signup3
    
    #set users attempts back to 4
    db = database.get_db()
    db.execute('UPDATE user SET attempts = 4 WHERE username = ?', (session['username'],))
    db.commit()
    
    return render_template("target.html")

@views.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('views.home'))

@views.route("/reset/<id>", methods=('GET', 'POST'))
def reset(id):

    db = database.get_db()

    res = bytes(id, 'utf-8')
    decID = fernet.decrypt(res).decode()

    username = db.execute('SELECT username FROM user WHERE id = ?', (decID,)).fetchone()
    fname = db.execute('SELECT fname FROM user WHERE id = ?', (decID,)).fetchone()
    lname = db.execute('SELECT lname FROM user WHERE id = ?', (decID,)).fetchone()

    session['username'] = username[0]
    session['fname'] = fname[0]
    session['lname'] = lname[0]
    session['reset'] = 'set'

    return redirect(url_for("views.signup2"))