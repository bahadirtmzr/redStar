# -*- coding: utf-8 -*-
#IMPORT REDSTAR
from redStar.interactiveMenu 	import *		#
from redStar.shellCreator 		import *		#Encryption Decryption 
from redStar.shellManagement 	import *		#add,delete, execute command zombie
from redStar.util 				import *		#

init()
try:
	interactiveMenu().cmdloop()
except KeyboardInterrupt:
	bye()