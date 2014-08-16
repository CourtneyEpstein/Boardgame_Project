import pymysql as mdb
import cPickle as pickle
import io, json
import pandas as pd
import numpy as np

def connect_to_MySQL():
    '''Define connection to the MySQL database, boardgamegeek'''
    path_getdata='/Users/athena/Insight/Boardgame_Project/getdata/'
    f=open(path_getdata+'mysql_password.txt','r')
    mysqlpass=f.read().split('\n')
    f.close()
    con = mdb.connect('localhost', mysqlpass[0], mysqlpass[1], 'boardgamegeek',charset='utf8')
    return con

path='/Users/athena/Insight/Boardgame_Project/recommend/'
preferences=pickle.load(open(path + "preferences_user_gt_10_game_gt_10.pkl", "rb" ))

game_id=np.unique(list(preferences['GAME_ID']))

con=connect_to_MySQL()
query='''SELECT GAME_ID,GAME_NAME FROM Games WHERE GAME_ID IN (%s)'''%(','.join(str(game) for game in game_id))
games=pd.io.sql.read_sql(query,con) 


games = dict(zip(games['GAME_ID'].values,games['GAME_NAME'].values))


with io.open('all_game_names.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(games, ensure_ascii=False)))