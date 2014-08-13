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
      - GAME NUMBER IN MATRIX AND GAME_ID
      - USER NUMBER IN MATRIX AND USER_NAME'''
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


class translate_games(object):
    '''PROVIDES DICTIONARIES TO CONVERT BETWEEN 
      - GAME_ID AND GAME_NAME'''
    def __init__(self,games):
        self.game_names=games['GAME_NAME'].values
        self.game_id=games['GAME_ID'].values
        self.game_name_to_id_dict=dict(zip(self.game_names,self.game_id))
        self.game_id_to_name_dict=dict(zip(self.game_id,self.game_names))
    def name_to_id(self,key):
        return self.game_name_to_id_dict[key]
    def id_to_name(self,key):
        return self.game_id_to_name_dict[key]
    def get_names(self):
        return self.game_names
    def get_ids(self):
        return self.game_ids

