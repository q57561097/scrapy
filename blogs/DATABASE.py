import MySQLdb.connector
conn = MySQLdb.connector.connect( user = 'root', passwd = 'password',)
cursor=conn.cursor()
try:
    cursor.execute('create database ph')
except:
    print('Database addtest exists!')
cursor.execute('create table sf (acctid int(11) primary key, money int(11))')