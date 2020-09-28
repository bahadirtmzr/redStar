import sqlite3
import uuid 
import time
import cmd
import random

from redStar.shellManagement 	import *
from redStar.interactiveMenu 	import *

 

conn = ""

def init():
	global conn
	conn = sqlite3.connect('sessions/redStar.db')
	sql = '''
		CREATE TABLE IF NOT EXISTS sessions (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			session_id TEXT,
			url TEXT,
			key TEXT,
			created_time TEXT NOT NULL
		);
	'''
	sql1 = '''
		CREATE TABLE IF NOT EXISTS logs (
			id TEXT PRIMARY KEY,
			session_id TEXT NOT NULL,
			user_id TEXT,
			pwd TEXT,
			ps TEXT,
			passwd_file TEXT,
			local_ip TEXT,
			sv_ip TEXT,
			log_time TEXT NOT NULL
		);
	'''

	cur = conn.cursor()
	cur.execute(sql)
	cur.execute(sql1)
	conn.commit()
	cur.close()
	print("[+] DB initialization success") 

def parse(arg):
	return tuple(map(str, arg.split()))

def bye():
	pre = "\n\n"
	texts=["🟊__redStar__🟊",
	"Nuclear Bomb Has Been Planted..", 
	"Shhh be loud",
	"Server is D0w\nConnection Lost[redStar]", 
	".. On line 0e6198 ..",
	"[redStar.exit loaded]",
	"\"I'm not a malware\"\n-redStar",
	"-----------",
	"E",
	"N",
	"I",
	"S",
	"A",
	"♡",
	"-----------"
	]
	r = random.randint(0, 6)
	print("\n\n"+texts[r]+"\n")



