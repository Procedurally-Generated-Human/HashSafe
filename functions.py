import hashlib
import os
import db_conn
import bcrypt
import uuid
import numpy as np
import base64
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC




def draw_line_top():
	print("----------------------------------------------------------------------------")
	print("")

def draw_line_bottom():
	print("")
	print("----------------------------------------------------------------------------")




def draw_logo():
	print("""    
----------------------------------------------------------------------------
----------------------------------------------------------------------------


##     ##    ###     ######  ##     ##  ######     ###    ######## ########   
##     ##   ## ##   ##    ## ##     ## ##    ##   ## ##   ##       ##       
##     ##  ##   ##  ##       ##     ## ##        ##   ##  ##       ##       
######### ##     ##  ######  #########  ######  ##     ## ######   ######   
##     ## #########       ## ##     ##       ## ######### ##       ##       
##     ## ##     ## ##    ## ##     ## ##    ## ##     ## ##       ##       
##     ## ##     ##  ######  ##     ##  ######  ##     ## ##       ########  

			Never Lose a Password Again  

----------------------------------------------------------------------------""")






def hash_master_password(plain_text_password):
	password = plain_text_password.encode('utf-8')
	salt = bcrypt.gensalt(rounds=16)
	key = bcrypt.hashpw(password, salt)
	return key, salt
	






def first_time_event():
	draw_line_top()
	print("It seems like it is your first time using HashSafe")
	print("Please enter a master password to begin, it is recommended to be strong and memorible")
	password_stored = False
	while password_stored == False:
		master_password_1 = input("Enter Master Password: ")
		master_password_2 = input("Re-enter Master Password: ")
		if master_password_1 == master_password_2:
			master_password = master_password_1
			key, salt = hash_master_password(master_password)
			db_conn.insert_into_key(key, salt)
			print("Password succesfully stored")
			password_stored = True
		else:
			print("Passwords do not match")
			draw_line_bottom()
	draw_line_bottom()






def verify_user():
	draw_line_top()
	master_password = input("Enter Your Password for Verification: ")
	master_password_og = db_conn.get_key()
	ss = bcrypt.checkpw(master_password.encode('utf-8'), master_password_og)
	if ss == True:
		master_password_verified = master_password
		password = master_password_verified.encode()
		salt = db_conn.get_salt()

		
		kdf = PBKDF2HMAC (
		algorithm = hashes.SHA256(),
		length = 32,
		salt = salt,
		iterations = 100000,
		backend = default_backend()
		)
		global master_key
		master_key = base64.urlsafe_b64encode (kdf.derive(password))
		pass
	else:
		print("Incorrect Password")
		draw_line_bottom()
		verify_user()
	draw_line_bottom()





def encrypt(string):
	secret = string.encode()
	f = Fernet(master_key)
	token = f.encrypt(secret)
	return token





def print_about():
	draw_line_top()
	print("Using modern encryption methods, HashSafe is able to keep your passwords")
	print("completly safe while also allowing you to easily access them in a user ")
	print("friendly interface.")
	print("")
	print("Technical details:")
	print("When entering your master password for the first time, HashSafe hashes it ")
	print("with a randonomly generated salt using bcrypt (your plain text master password is")
	print("never stored), using the same master password it also genrates a key (using 100,000")
	print("iterations of Sha256) for encrypting and decrypting all of your account passwords")
	print("which are stored as encrypted bytes in the database.")
	print("The Key is also never saved and is only created when you enter you the master password")
	print("")
	print("HashSafe is developed by Procedurally Generated Human.")
	draw_line_bottom()






def exit_program():
	sys.exit()





def add_new_password():
	draw_line_top()
	print("            Add New Password")
	print("")
	website = input("Website Name: ")
	url = input("Website URL: ")
	username = input("Website Username: ")
	email = input("Website Email: ")
	password  = input("Website Password: ")
	print("")
	confirmation = input("Is this correct(Y/N): ").lower()
	if confirmation == "y":
		encrypted_password = encrypt(password)
		db_conn.insert_account_data(website, url, username, email, encrypted_password)
		print("New Password Added")
	else:
		add_new_password()
		draw_line_bottom()
	draw_line_bottom()





def show_password():
	draw_line_top()
	query = input("Website name or URL: ")
	print("")
	data = db_conn.find_password(query)
	matrix = list(map(list,data))
	f = Fernet(master_key)
	for e in range(0,len(matrix)):
		matrix[e][5] = f.decrypt(matrix[e][5]).decode()
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print ('\n'.join(table))
	draw_line_bottom()





def show_all_passwords():
	draw_line_top()
	data = db_conn.get_all_passwords()
	matrix = list(map(list,data))
	f = Fernet(master_key)
	for e in range(0,len(matrix)):
		matrix[e][5] = f.decrypt(matrix[e][5]).decode()
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print ('\n'.join(table))
	draw_line_bottom()





def main_menu_event():
	draw_line_top()
	print("                          Welcome To HashSafe              ")
	print("")
	print("            +-------------------+------------------------+")
	print("            | 1 = Find Password | 2 = List All Passwords |")
	print("            +-------------------+-----------+------------+")
	print("            | 3 = New Password  | 4 = About |  5 = Quit  |")
	print("            +-------------------+-----------+------------+")
	quit = True
	draw_line_bottom()
	while quit == True:
		draw_line_top()
		menu_choice = input("What Do You Want To Do? : ")
		if menu_choice == "1":
			draw_line_bottom()
			show_password()
		elif menu_choice == "3":
			draw_line_bottom()
			add_new_password()
		elif menu_choice == "2":
			draw_line_bottom()
			show_all_passwords()
		elif menu_choice == "4":
			draw_line_bottom()
			print_about()
		elif menu_choice == "5":
			draw_line_bottom()
			exit_program()
		else:
			print("Command Not Recognized")
	draw_line_bottom()
