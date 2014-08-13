import pymysql as mdb
import pandas as pd


def connect_to_MySQL():
    '''Define connection to the MySQL database, boardgamegeek'''
    path_getdata='/Users/athena/Insight/Boardgame_Project/getdata/'
    f=open(path_getdata+'mysql_password.txt','r')
    mysqlpass=f.read().split('\n')
    f.close()
    con = mdb.connect('localhost', mysqlpass[0], mysqlpass[1], 'boardgamegeek',charset='utf8')
    return con

    
class translator(object):
    '''PROVIDES DICTIONARIES TO CONVERT BETWEEN 
#      - GAME_ID AND GAME_NAME
#      - USER_ID AND USER_NAME'''
    def __init__(self,average_ratings):
        levels_user=average_ratings.index.levels[0].values
        levels_game=average_ratings.index.levels[1].values
        unique_games=range(len(levels_game))
        unique_users=range(len(levels_user))

        self.game_id_to_num_dict=dict(zip(levels_game,unique_games))
        self.game_num_to_id_dict=dict(zip(unique_games,levels_game))

        self.user_id_to_num_dict=dict(zip(levels_user,unique_users))
        self.user_num_to_id_dict=dict(zip(unique_users,levels_user))
    def value2index(self,key,user=False,game=False):
        if(user==game):
            sys.exit("Please select whether you want to convert users or games")
        elif(user==True):
            return self.user_id_to_num_dict[key]
        else:
            return self.game_id_to_num_dict[key]
    def index2value(self,key,user=False,game=False):
        if(user==game):
            sys.exit("Please select whether you want to convert users or games")
        elif(user==True):
            return self.user_num_to_id_dict[key]
        else:
            return self.game_num_to_id_dict[key]

