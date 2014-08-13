import pymysql as mdb
import cPickle as pickle
import pandas as pd
from useful import *
import scipy.sparse as sparse

def get_input(like_input_game_string,dislike_input_game_string,translate,translate_game):
    # print input_game_string
    '''Will have to parse game text here'''
    like_input_game=like_input_game_string
    dislike_input_game=dislike_input_game_string
    like_rating=8
    dislike_rating=2
    print like_input_game
    print len(like_input_game),len(dislike_input_game)
    # games=[translate.value2index(translate_game.name_to_id(game),game=True) for game in like_input_game]
    # ratings
    # tmp1=[like_rating]*len(like_input_game)
    # tmp1=[like_rating]*len(like_input_game)

    # print games
    # games=scipy.sparse.coo_matrix((data_rating,(labels_user,labels_game)),shape=(len(levels_user),len(levels_game)))


    # if(input_game_name in translate.allowed_game_names()):
#         return translate.name_to_id(input_game_name)
#     else:
#         sys.exit()

'''Load translator'''
try:
    translate
except:
    print "Loading translator"
    path="/Users/athena/Insight/Boardgame_Project/recommend/"
    translate=pickle.load(open( path+"translator.pkl", "rb" ))
'''Load game translator'''
try:
    translate_game
except:
    print "Loading game translator"
    path="/Users/athena/Insight/Boardgame_Project/recommend/"
    translate_game=pickle.load(open( path+"translator_games.pkl", "rb" ))
'''Load similarity mtrix'''
try:
    cosine_similarity_gameXgame
except:
    print "Loading cosine similarity matrix"
    cosine_similarity_gameXgame = pickle.load(open( path+"game_recommendation_matrix_cosine_users_gt_10_ratings.pkl", "rb" ))
    print "Done loading cosine similarity matrix"

like_input_game_string=['Apples to Apples','The Settlers of Catan','Stone Age']
dislike_input_game_string=['Monopoly']
input_game=get_input(like_input_game_string,dislike_input_game_string,translate,translate_game)
# input_game_id=


# cosine_similarity_gameXgame*



# import numpy as np
# import pymysql as mdb
# import cPickle as pickle
# import sys

# def connect_to_MySQL():
#     '''Define connection to the MySQL database, boardgamegeek'''
#     path_getdata='/Users/athena/Insight/Boardgame_Project/getdata/'
#     f=open(path_getdata+'mysql_password.txt','r')
#     mysqlpass=f.read().split('\n')
#     f.close()
#     con = mdb.connect('localhost', mysqlpass[0], mysqlpass[1], 'boardgamegeek',charset='utf8')
#     return con

    
# class translator(object):
#     '''PROVIDES DICTIONARIES TO CONVERT BETWEEN GAME_ID AND GAME_NAME'''
#     def __init__(self,con):
#         with con: 
#             cur = con.cursor()
#             cur.execute('SELECT GAME_ID,GAME_NAME FROM Games LIMIT 100;')
#             rows = cur.fetchall()
#             self.name_to_id_dict={ game_name:game_id  for game_id,game_name in rows}
#             self.id_to_name_dict={ game_id:game_name  for game_id,game_name in rows}
#             self.game_id_to_index_dict={game_id:i for i,game_id in enumerate(self.allowed_game_ids())}
#     def name_to_id(self,GAME_NAME):
#         return self.name_to_id_dict[GAME_NAME]
#     def id_to_name(self,GAME_ID):
#         return self.id_to_name_dict[GAME_ID]
#     def allowed_game_names(self,):
#         return self.name_to_id_dict.keys()
#     def allowed_game_ids(self,):
#         return self.id_to_name_dict.keys()
#     def game_id_to_index(self,GAME_ID):
#         return self.game_id_to_index_dict[GAME_ID]
#     def __getitem__(self,key):
#       '''This allows you to type self['name'] rather than self.name
#       it uses the dictionary for the object'''
#       if key in self.__dict__.keys():
#          return self.__dict__[key]
#       if key in self.keys:
#          return self.data[key]

# def get_input(translate,input_game_name):
#     if(input_game_name in translate.allowed_game_names()):
#         return translate.name_to_id(input_game_name)
#     else:
#         sys.exit()

# def make_recommendation(input_game_name):
#     con=connect_to_MySQL()
#     '''DEFINE THE CONVERSION BETWEEN GAME_ID AND GAME_NAME'''
#     try:
#         translate
#     except:
#         translate=translator(con)
    
#     input_game=get_input(translate,input_game_name)

#     path="/Users/athena/Insight/Boardgame_Project/recommend/"
#     # output=pickle.load(open( path+"game_recommendation_matrix.pkl", "rb" ))
#     output=pickle.load(open( path+"game_recommendation_matrix_cosine.pkl", "rb" ))
    
#     index_input_game=translate.game_id_to_index(input_game)
#     output_line=output[index_input_game]
    
#     idx_nonzero=list(np.where(output_line > 0.)[0])
#     '''So you don't recommend the input game'''
#     idx_nonzero.remove(index_input_game)
    
#     return [translate.allowed_game_ids()[idx_nonzero[i]] for i in np.argsort(output_line[idx_nonzero])[-5:]]
    
