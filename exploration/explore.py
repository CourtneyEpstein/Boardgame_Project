import numpy as np
import MySQLdb as mdb
import pandas as pd

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
    cur = con.cursor()
    cur.execute("SELECT GAME_NAME,GAME_ID,USER_NAME,USER_RATING FROM Preferences WHERE GAME_NAME IN ('The Settlers of Catan','Lost Cities')")
    rows = cur.fetchall()
tmp=np.array([row for row in rows])

preferences=pd.DataFrame(tmp,columns=['GAME_NAME','GAME_ID','USER_NAME','USER_RATING'])
tmp2=pd.pivot_table(preferences, values='USER_RATING', index=['USER_NAME'],columns=['GAME_NAME','GAME_ID'])
print tmp2