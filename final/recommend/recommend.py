import pymysql as mdb
import cPickle as pickle
import numpy as np
import pandas as pd
from useful import *
import scipy.sparse as sparse
import json



class rec_engine():
    def __init__(self):
        path_to_static='/Users/athena/Insight/Boardgame_Project/website/app/static/'
        self.path_to_similarity='/Users/athena/Insight/Boardgame_Project/final/similarity1/'
        self.path_to_game_info='/Users/athena/Insight/Boardgame_Project/final/recommend/'
        json_data=open(path_to_static+'all_game_names.json')
        self.game_id_to_name_dict = json.load(json_data)
        self.game_name_to_id_dict = dict(zip(self.game_id_to_name_dict.values(),self.game_id_to_name_dict.keys()))
        self.input_game=dict()
        self.input_time=0
        self.input_num_players=0
    def add_input_game(self,input_game_name,rating):
        if(input_game_name in self.game_id_to_name_dict.values()):
            game_id=self.game_name_to_id_dict[input_game_name]
            self.input_game[int(game_id)]=rating
        else:
            sys.exit()
    def add_input_game_id(self,input_game_id,rating):
        if(input_game_id in self.game_id_to_name_dict.keys()):
            self.input_game[int(input_game_id)]=rating
        else:
            sys.exit()
    def add_input_time(self,input_time):
        self.input_time=input_time
    def add_input_num_players(self,input_num_players):
        self.input_num_players=input_num_players
    def get_input_game(self):
        return self.input_game
    def get_games_input_time(self):
        if(int(self.input_time)>0):
            return pickle.load(open(self.path_to_game_info+"playing_time_{0}.pkl".format(self.input_time),'rb'))
        else:
            return None
    def get_games_input_num_players(self):
        if(int(self.input_num_players)>0):
            return pickle.load(open(self.path_to_game_info+"num_players_{0}.pkl".format(self.input_num_players),'rb'))
        else:
            return None
    def get_similarity(self,game_id):
        return pickle.load(open(self.path_to_similarity+'{0}.pkl'.format(game_id),'rb'))
    def recommend(self,):
        '''STEP 1: GET THE SIMILARITY MATRIX, BUT ONLY FOR THE COLUMNS WE CARE ABOUT'''
        for i,game_id in enumerate(self.get_input_game().keys()):
            sim_dict=self.get_similarity(game_id)
            if(i==0):
                game_id_list=np.array(sim_dict.keys())
                sim_matrix=np.zeros((len(game_id_list),len(self.get_input_game())))
                user_ratings=np.zeros(len(self.get_input_game()))
            sim_matrix[:,i]=sim_dict.values()
            user_ratings[i]=self.get_input_game()[game_id]
        sim_ratings = sim_matrix.dot(user_ratings)
        weights     = np.sum(user_ratings,axis=0)
        '''GET THE WEIGHTED AVERAGE'''
        '''GETTING THE SIMILARITY WEIGHTED BY THE RANKINGS'''
        unordered=sim_ratings/weights
        '''SORT THE UNORDERED LIST TO GET RANKINGS'''
        idx=np.argsort(unordered)[::-1]
        order_dict=dict(zip(game_id_list[idx],range(len(game_id_list))))
        '''DON'T RECOMMEND ONE OF THE INPUT GAMES'''
        remove_inputs=np.setdiff1d(game_id_list,np.array(self.get_input_game().keys()))
        '''RESTRICT OUTPUT TO GAMES WITH THE REQUESTED PLAYING TIME'''
        allowed_time=self.get_games_input_time()
        if(allowed_time!=None):
            filter_time=np.intersect1d(remove_inputs,allowed_time)
        else:
            filter_time=remove_inputs
        '''RESTRICT OUTPUT TO GAMES WITH THE REQUESTED NUMBER OF PLAYERS'''
        allowed_num_players=self.get_games_input_num_players()
        if(allowed_num_players!=None):
            filter_num_players=np.intersect1d(filter_time,allowed_num_players)
        else:
            filter_num_players=filter_time
        outlist= sorted(filter_num_players,key=lambda game_id: order_dict[game_id])
        return outlist[0:min(10,len(outlist))]


def test():
    recommendation=rec_engine()
    recommendation.add_input_game('Apples to Apples',10)
    recommendation.add_input_game('The Settlers of Catan',10)
    recommendation.add_input_time(3)
    # print recommendation.get_input_game()
    recs = recommendation.recommend()
    print recs

    
# test()
