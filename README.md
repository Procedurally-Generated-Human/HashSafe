![alt text](https://github.com/Procedurally-Generated-Human/HashSafe/blob/main/Screen%20Shot%202021-10-03%20at%2010.41.31%20AM.png)

Technical details:
	When entering your master password for the first time, HashSafe hashes it
	with a randonomly generated salt using bcrypt (your plain text master password is
	never stored), using the same master password it also genrates a key (using 100,000
	iterations of Sha256) for encrypting and decrypting all of your account passwords
	which are stored as encrypted bytes in the database.
	The Key is also never saved and is only created when you enter you the master password.
	
	
	
