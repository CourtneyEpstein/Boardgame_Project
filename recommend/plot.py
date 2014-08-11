import numpy as np
import pymysql as mdb
import cPickle as pickle
import matplotlib.pyplot as plt

def connect_to_MySQL():
    '''Define connection to the MySQL database, boardgamegeek'''
    path_getdata='/Users/athena/Insight/Boardgame_Project/getdata/'
    f=open(path_getdata+'mysql_password.txt','r')
    mysqlpass=f.read().split('\n')
    f.close()
    con = mdb.connect('localhost', mysqlpass[0], mysqlpass[1], 'boardgamegeek',charset='utf8')
    return con

con=connect_to_MySQL()
with con:
    cur=con.cursor()
    cur.execute("SELECT USER_NAME,COUNT(DISTINCT GAME_ID) AS tmp FROM PREFERENCES GROUP BY USER_NAME;")
    rows=cur.fetchall()

n_ratings_per_game=[float(num) for name,num in rows ]

plt.hist(n_ratings_per_game)