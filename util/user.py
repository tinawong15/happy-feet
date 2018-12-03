#code to create user table in database.db
import sqlite3
from passlib.hash import sha256_crypt

DB_FILE = "data/database.db"

# creates table called users
def createTable():
    ''' This function creates Users table in database with column names id, username, and password.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT, question TEXT, answer TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tags (user TEXT, tag TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS cities (user TEXT, city TEXT)")
    db.commit()
    db.close()

# if username already exists, returns false. otherwise inserts a row in users, returns true.
def register(usr, psw, q, a):
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

# returns true if username and password match, false otherwise
def authenticate(usr, psw):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users")
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
    params = (psw, usr)
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

# given a user, returns a list of all the saved tags for news
def getTags(usr):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM " + usr + "_tags")
    l = [];
    for row in data:
        l.append(row[0])
    db.close()
    return l

# given a user, returns a list of all the bookmarked cities for weather
def getLocations(usr):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM " + usr + "_locations")
    l = [];
    for row in data:
        l.append(row[0])
    db.close()
    return l

# given a user, returns a dictionary with all stats associated with the user
def getStats(usr):
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
