#code to create user table in database.db
import sqlite3
from passlib.hash import sha256_crypt

DB_FILE = "data/database.db"

def createTable():
    ''' This function creates a Users table in database with column names username, password, security question, and answer.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT, question TEXT, answer TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tags (user TEXT, tag TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS cities (user TEXT, city TEXT)")
    db.commit()
    db.close()

def register(usr, psw, q, a):
    '''This function adds the user to the database.
    If username already exists, returns false. Otherwise, the function inserts a row in users and returns true.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users;")
    for row in data:
        if usr == row[0]:
            return False
    params = (usr, sha256_crypt.hash(psw), q, a)
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", params)
    c.execute("CREATE TABLE " + usr + "_tags (tag TEXT)")
    c.execute("CREATE TABLE " + usr + "_locations (location TEXT)")
    db.commit()
    db.close()
    return True

def authenticate(usr, psw):
    '''This function checks user login. If username and password match, the function returns true. The function returns false otherwise.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users")
    #checks if the usernames and encrypted passwords match
    for row in data:
        if row[0] == usr and sha256_crypt.verify(psw, row[1]):
            db.close()
            return True
    db.close()
    return False

# trivial
def resetPassword(usr, psw):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    params = (sha256_crypt.hash(psw), usr)
    c.execute("UPDATE users SET password = ? WHERE user = ?", params)
    db.commit()
    db.close()

def getQuestion(usr):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users")
    for row in data:
        if row[0] == usr:
            db.close()
            return row[2]
    db.close()
    return -1

def checkAnswer(usr, ans):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users")
    for row in data:
        if row[0] == usr:
            db.close()
            return row[3] == ans

def addTag(usr, tag):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute('SELECT * FROM ' + usr + '_tags')
    for row in data:
        if row[0] == tag:
            db.close()
            return False
    c.execute('INSERT INTO ' + usr + '_tags VALUES ("' + tag + '")' )
    db.commit()
    db.close()
    return True

def addLoc(usr, loc):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute('SELECT * FROM ' + usr + '_locations')
    for row in data:
        if row[0] == loc:
            db.close()
            return False
    c.execute('INSERT INTO ' + usr + '_locations VALUES ("' + loc + '")' )
    db.commit()
    db.close()
    return True

def removeTag(usr, tag):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM ' + usr + '_tags WHERE tag = "' + tag + '"');
    db.commit()
    db.close()

def removeLoc(usr, tag):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM ' + usr + '_locations WHERE location = "' + tag + '"');
    db.commit()
    db.close()

def getTags(usr):
    '''Given a user, this function returns a list of all the saved tags for news'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM " + usr + "_tags")
    l = [];
    for row in data:
        l.append(row[0])
    db.close()
    return l

def getLocations(usr):
    '''Given a user, this function returns a list of all the bookmarked cities for weather.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM " + usr + "_locations")
    l = [];
    for row in data:
        l.append(row[0])
    db.close()
    return l

def getStats(usr):
    '''Given a user, this function returns a dictionary with all statistics associated with the user.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users")
    d = {}
    for row in data:
        if usr == row[0]:
            d['password'] = row[1]
            d['question'] = row[2]
            d['answer'] = row[3]
            d['tags'] = getTags(usr)
            d['locations'] = getLocations(usr)
            db.close()
            return d

#createTable()
