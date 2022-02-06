import mysql.connector

##---------------------------------------------------------
# Use the following code to create a database (for first time use) and then again comment 
# the code

# db = mysql.connector.connect(   # enter your local mysql server details (user and passwd)
# 	host = "localhost",
# 	user = "chessdb",
# 	passwd = "chess",
# 	)

# mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE maindatabase")

##---------------------------------------------------------

db = mysql.connector.connect(   # enter your local mysql server details (user and passwd)
	host = "localhost",
	user = "chessdb",
	passwd = "chess",
	database = "maindatabase"  
	)                          

mycursor = db.cursor(buffered=True)
cursorformoves = db.cursor(buffered=True) 