import numpy as np
import pymysql as mdb
import cPickle as pickle
import sys

def connect_to_MySQL():
    '''Define connection to the MySQL database, boardgamegeek'''
    path_getdata='/Users/athena/Insight/Boardgame_Project/getdata/'
    f=open(path_getdata+'mysql_password.txt','r')
    mysqlpass=f.read().split('\n')
    f.close()
    con = mdb.connect('localhost', mysqlpass[0], mysqlpass[1], 'boardgamegeek',charset='utf8')
    return con

    
class translator(object):
    '''PROVIDES DICTIONARIES TO CONVERT BETWEEN GAME_ID AND GAME_NAME'''
    def __init__(self,con):
        with con: 
            cur = con.cursor()
            cur.execute('SELECT GAME_ID,GAME_NAME FROM Games LIMIT 100;')
            rows = cur.fetchall()
            self.name_to_id_dict={ game_name:game_id  for game_id,game_name in rows}
            self.id_to_name_dict={ game_id:game_name  for game_id,game_name in rows}
            self.game_id_to_index_dict={game_id:i for i,game_id in enumerate(self.allowed_game_ids())}
    def name_to_id(self,GAME_NAME):
        return self.name_to_id_dict[GAME_NAME]
    def id_to_name(self,GAME_ID):
        return self.id_to_name_dict[GAME_ID]
    def allowed_game_names(self,):
        return self.name_to_id_dict.keys()
    def allowed_game_ids(self,):
        return self.id_to_name_dict.keys()
    def game_id_to_index(self,GAME_ID):
        return self.game_id_to_index_dict[GAME_ID]
    def __getitem__(self,key):
      '''This allows you to type self['name'] rather than self.name
      it uses the dictionary for the object'''
      if key in self.__dict__.keys():
         return self.__dict__[key]
      if key in self.keys:
         return self.data[key]

# def get_input(translate):
#     input_game='RoboRally'
#     if(input_game in translate.allowed_game_names()):
#         return translate.name_to_id(input_game)
#     else:
#         sys.exit()



con=connect_to_MySQL()
'''DEFINE THE CONVERSION BETWEEN GAME_ID AND GAME_NAME'''
try:
    translate
except:
    translate=translator(con)


'''Set allowed games (first 500)'''
allowed_games=[game for game in translate.allowed_game_ids()]

with con:
    cur = con.cursor()
    cur.execute("SELECT DISTINCT USER_NAME FROM Preferences WHERE GAME_ID < %s;",max(allowed_games))
    row_names = cur.fetchall()
    all_users=[user_name[0] for user_name in row_names]

num_users=1000
np.random.seed(seed=1)
users=np.random.choice(all_users,size=num_users, replace=False)

with con: 
    cur = con.cursor()
    '''Select unique users that have liked the games provided in the input'''
    user_game=np.zeros((num_users,len(allowed_games)))    
    for i in range(len(users)):
        print i,users[i]
        cur.execute("SELECT GAME_ID,USER_RATING FROM Preferences WHERE USER_NAME = %s AND GAME_ID < %s",[users[i],max(allowed_games)])
        row_games=cur.fetchall()
        for game_id,rating in row_games:
            jj=translate.game_id_to_index(game_id)
            user_game[i,jj]=rating


# XtX=np.dot(user_game.T,user_game)
# mag_Xt= np.dot(user)
# mag_X =

cosine_matrix=np.zeros((len(allowed_games),len(allowed_games))) 
for i in range(len(allowed_games)):
    for j in range(len(allowed_games)):
        a=user_game.T[i,:]
        b=user_game[:,j]
        len_a=np.sqrt(np.dot(a,a))
        len_b=np.sqrt(np.dot(b,b))
        if(len_a>0 and len_b >0):
            cosine_matrix[i,j]=np.dot(a,b)/(len_a*len_b)




# output=np.dot(user_game.T,user_game)/(100.*num_users)
# pickle.dump(output,open( "game_recommendation_matrix.pkl", "wb" ))
pickle.dump(cosine_matrix,open( "game_recommendation_matrix_cosine.pkl", "wb" ))

