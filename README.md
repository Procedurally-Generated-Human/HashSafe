![alt text](https://github.com/Procedurally-Generated-Human/HashSafe/blob/main/Screen%20Shot%202021-10-03%20at%2010.41.31%20AM.png)

HashSafe is a terminal based Python program that stores your passwords by encrypting them with the hashed version of your master password.

Technical details:
	When entering your master password for the first time, HashSafe hashes it
	with a randomly generated salt using bcrypt (your plain text master password is
	never stored), using the same master password it also genrates a key (using 100,000
	iterations of Sha256) for encrypting and decrypting all of your account passwords
	which are stored as encrypted bytes in the database.
	The Key is also never saved and is only created when you enter your master password.
	
	
	
