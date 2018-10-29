import os

class Config:
	# secret code for encoding ...
	SECRET_CODE = os.environ.get('SECRET_CODE')
	# mysql
	MYSQL_HOST = os.environ.get('MYSQL_HOST')
	MYSQL_USER = os.environ.get('MYSQL_USER')
	MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
	MYSQL_DB = os.environ.get('MYSQL_DB')