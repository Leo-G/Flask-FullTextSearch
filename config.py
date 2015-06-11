#DATABASE SETTINGS
db_username = 'postgres'
db_password = 'qwedsa@123'
db_name = 'search2'
db_hostname = 'localhost'

DEBUG = True
PORT = 5000
HOST = "172.16.189.28"
SQLALCHEMY_ECHO = True
SECRET_KEY = "c1987yhue25-88ec-4ec2-b2fe-4c213413jki89"
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=db_username,
                                                                                        DB_PASS=db_password,
                                                                                        DB_ADDR=db_hostname,
                                                                                        DB_NAME=db_name)
