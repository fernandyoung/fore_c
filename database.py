import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

#connection
class connection(object):
	"""docstring for connection"""
	def __init__(self):
		self.connection=mysql.connector.connect(
			host = 'containers-us-west-63.railway.app',
			user = 'root',
			port = '6872',
			password = 'v42I0qPogHcoUEdB9rHG',
			database = 'railway'
			)

	#check username
	def check_username(self, username):
		cursor = self.connection.cursor()
		cursor.execute('SELECT * FROM user WHERE username=%s',(username,))
		akun = cursor.fetchone()
		return akun

	def insert(self, username, password):
		cursor = self.connection.cursor()
		cursor.execute('INSERT INTO user(`username`, `password`, `type`) VALUES(%s,%s,0)',(username,generate_password_hash(password)))
		insert = self.connection.commit()
		return insert
