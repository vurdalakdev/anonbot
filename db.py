import sqlite3, time

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(userid INT, utcm INT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS msgs(msg CHAR, utcm INT, toid INT)""")


def create_user(userid):
	cursor.execute(f"""INSERT INTO users (userid, utcm) SELECT {userid}, {time.time()} WHERE NOT EXISTS (SELECT * FROM users WHERE userid = {userid});""")
	db.commit()

def get_user(userid):
	cursor.execute(f"""SELECT * FROM users WHERE userid={userid};""")
	return cursor.fetchone()

def get_users():
	cursor.execute(f"""SELECT * FROM users;""")
	return cursor.fetchall()

def add_msg(message, userid):
	cursor.execute(f"""INSERT INTO msgs (msg, utcm, toid) SELECT '{message}', {time.time()}, {userid} WHERE NOT EXISTS (SELECT * FROM msgs WHERE msg = '{message}');""")
	db.commit()

def get_all_msgs(userid):
	cursor.execute(f"""SELECT * FROM msgs WHERE toid={userid};""")
	return cursor.fetchall()