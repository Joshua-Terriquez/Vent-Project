import sqlite3
from sqlite3 import Error

def openConnection(dbFile):
    try:
        conn = sqlite3.connect(dbFile)
        print("Success opening database.")
    except Error as e:
        print(e)
    return conn

def closeConnection(_conn, dbFile):
    print("Close Database: ", dbFile)
    try:
        _conn.close()
        print("Success!")
    except Error as e:
        print(e)

def createTables(conn):
    cur = conn.cursor()
    try:
        tables = """
        DROP TABLE IF EXISTS Users;
        DROP TABLE IF EXISTS userPosts;
        CREATE TABLE Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email           STRING  NOT NULL UNIQUE,
            password        STRING  NOT NULL,
            pubKey          STRING  UNIQUE NOT NULL,
            privateKey      STRING  UNIQUE NOT NULL,
            CHECK (email LIKE '%@%.%')
        );

        CREATE TABLE userPosts (
            post_id     INTEGER     PRIMARY KEY AUTOINCREMENT,
            date        DATETIME    NOT NULL
                                    DEFAULT (datetime('now','localtime')),
            user        INTEGER     NOT NULL
                                    REFERENCES Users(user_id),
            postStr     STRING      NOT NULL
        );
        """
        cur.executescript(tables)
        conn.commit()
        print("Tables created")
    except Error as e:
        print(e)

def insertUser(conn, newUser):
    cur = conn.cursor()
    try:
        sql = """
            INSERT INTO Users (email, password, pubKey, privateKey)
            VALUES (?, ?, ?, ?);"""
        args = [newUser[0], newUser[1], newUser[2], newUser[3]]
        cur.execute(sql, args)
        conn.commit()
        print("added new user")
    except Error as e:
        print(e)

def createPost(conn, post):
    cur = conn.cursor()
    try:
        sql = """INSERT INTO userPosts(user, postStr)
                VALUES (?, ?)
        """
        args = [post[0], post[1]]
        cur.execute(sql, args)
        conn.commit()
        print("new post added.")
    except Error as e:
        print(e)


def main():
    database = r'databse.db'
    conn = openConnection(database)
    createTables(conn)

    user =( ['newEmail@gmail.com', 'drowssap', 'somePubKey', 'somePrivateKey'],
            ['anotherEmail@gmail.com', 'some_password', 'pubkey2', 'keykey'])
    post = ([1, "Today is a nice day."])
    post2 = ([1, "Final Project."])
    for x in user:
        insertUser(conn, x)
    createPost(conn, post)
    createPost(conn, post2)


    closeConnection(conn,database)

if __name__ == '__main__':
    main()