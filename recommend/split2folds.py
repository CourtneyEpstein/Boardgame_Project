import numpy as np
import pymysql as mdb
import cPickle as pickle
import sys
import pandas as pd
import scipy.sparse as sparse
import math
from useful import *
import sklearn.cross_validation

def get_similarity_matrix(training):
    print "in function"
    # '''Define the translation between
    # user=True: row # (index) and user name (value); OR
    # game=True: column # (index) and game id (value)'''
    translate=translator(training)
    # '''Use the pandas multiindex to define the coordinates of the array'''
    levels_user=list(training.index.levels[0])
    levels_game=list(training.index.levels[1])
    labels_user=list(training.index.labels[0])
    labels_game=list(training.index.labels[1])
    # ''' and the values, averaged if there are multiple ratings by the same user per game'''
    data_rating=training.ix[:,0].values
    # '''This is a matrix with users on the rows and games on the columns'''
    ratings=sparse.coo_matrix((data_rating,(labels_user,labels_game)),shape=(len(levels_user),len(levels_game)))
    # '''Once a matrix has been constructed, convert to CSR or CSC format for fast arithmetic and matrix vector operations'''
    userXgame=ratings.tocsr()
    gameXgame=(userXgame.T).dot(userXgame)
    # '''The sum of squares is the entry along the diagonal
    # Cosine similarity is divided by the magnitude of the vector
    # To get the magnitude, take the sqrt of the dot product (i.e. the diagonal)
    # Compute this for every entry on the diagonal'''
    diagonals = [1./math.sqrt(gameXgame[i,i]) if(gameXgame[i,i]!=0) else 1. for i in range(len(levels_game))]
    # '''Convert this to a sparse matrix'''
    diag_norm = sparse.diags(diagonals,offsets=0)
    cosine_similarity_gameXgame = diag_norm.dot(gameXgame).dot(diag_norm)
    # '''Output resulting similarity matrix to file'''
    # pickle.dump(cosine_similarity_gameXgame,open( "game_recommendation_matrix_cosine_users_gt_10_ratings.pkl", "wb" ))
    return translate,cosine_similarity_gameXgame

con=connect_to_MySQL()

try:
    preferences
except:
    # print "Reading from MySQL..."
    # # preferences=pd.io.sql.read_sql('SELECT P.USER_NAME,P.GAME_ID,P.USER_RATING FROM Preferences AS P LEFT JOIN (SELECT USER_NAME,COUNT(DISTINCT GAME_ID) AS CNT FROM Preferences GROUP BY USER_NAME) as TMP ON P.USER_NAME=TMP.USER_NAME WHERE TMP.CNT BETWEEN 10 AND 100;',con)
    # preferences=pd.io.sql.read_sql('''SELECT P.USER_NAME,P.GAME_ID,P.USER_RATING FROM Preferences AS P 
    #     LEFT JOIN (SELECT USER_NAME,COUNT(DISTINCT GAME_ID) AS CNT FROM Preferences GROUP BY USER_NAME) as CNTUSER ON P.USER_NAME=CNTUSER.USER_NAME 
    #     LEFT JOIN (SELECT GAME_ID,COUNT(DISTINCT USER_NAME) AS CNT FROM Preferences GROUP BY GAME_ID)   as CNTGAME ON P.GAME_ID=CNTGAME.GAME_ID 
    #     WHERE CNTUSER.CNT > 10 AND CNTGAME.CNT > 10 ;''',con)
    # print "Done reading from MySQL."
    # print "Pickling preferences"
    # pickle.dump(preferences,open( "preferences_user_gt_10_game_gt_10.pkl", "wb" ))
    # print "Done pickling"
    print '''loading preferences from pickled file'''
    preferences=pickle.load(open( "preferences_user_gt_10_game_gt_10.pkl", "rb" ))
    print '''preferences loaded'''
average_ratings=preferences.groupby(['USER_NAME','GAME_ID']).mean()
'''Use the pandas multiindex to define the coordinates of the array'''
levels_user=np.array(average_ratings.index.levels[0])
levels_game=np.array(average_ratings.index.levels[1])
# labels_user=list(average_ratings.index.labels[0])
# labels_game=list(average_ratings.index.labels[1])
# pickle.dump(translate,open( "translator.pkl", "wb" ))

# there are 71321 users that have rated > 10 games 
# and 15602 games that have been rated by > 10 users
print "split to folds"
f1,f2,f3,f4,f5=sklearn.cross_validation.KFold(len(levels_user),n_folds=5,shuffle=True)
print "Done splitting"
# user_names_training1=levels_user[f1[0]]
# user_names_training2=levels_user[f2[0]]
# user_names_training3=levels_user[f3[0]]
# user_names_training4=levels_user[f4[0]]
# user_names_training5=levels_user[f5[0]]
user_names_fold1 =levels_user[f1[1]]
user_names_fold2 =levels_user[f2[1]]
user_names_fold3 =levels_user[f3[1]]
user_names_fold4 =levels_user[f4[1]]
user_names_fold5 =levels_user[f5[1]]
idx = pd.IndexSlice
print "Set 1"
fold1=average_ratings.loc(axis=0)[idx[user_names_fold1,:]]
pickle.dump([fold1],open( "fold1.pkl", "wb" ))
print "Set 2"
fold2=average_ratings.loc(axis=0)[idx[user_names_fold2,:]]
pickle.dump([fold2],open( "fold2.pkl", "wb" ))
print "Set 3"
fold3=average_ratings.loc(axis=0)[idx[user_names_fold3,:]]
pickle.dump([fold3],open( "fold3.pkl", "wb" ))
print "Set 4"
fold4=average_ratings.loc(axis=0)[idx[user_names_fold4,:]]
pickle.dump([fold4],open( "fold4.pkl", "wb" ))
print "Set 5"
fold5=average_ratings.loc(axis=0)[idx[user_names_fold5,:]]
pickle.dump([fold5],open( "fold5.pkl", "wb" ))


# print "Done with sets"
# print "Get similarity1"
# translate1,similarity1=get_similarity_matrix(training1)
# print "Pickle similarity1"
# pickle.dump([translate1,similarity1],open( "similarity1.pkl", "wb" ))
# print "Get similarity2"
# translate2,similarity2=get_similarity_matrix(training2)
# print "Pickle similarity2"
# pickle.dump([translate2,similarity2],open( "similarity2.pkl", "wb" ))
# print "Get similarity3"
# translate3,similarity3=get_similarity_matrix(training3)
# print "Pickle similarity3"
# pickle.dump([translate3,similarity3],open( "similarity3.pkl", "wb" ))
# print "Get similarity4"
# translate4,similarity4=get_similarity_matrix(training4)
# print "Pickle similarity4"
# pickle.dump([translate4,similarity4],open( "similarity4.pkl", "wb" ))
# print "Get similarity5"
# translate5,similarity5=get_similarity_matrix(training5)
# print "Pickle similarity5"
# pickle.dump([translate5,similarity5],open( "similarity5.pkl", "wb" ))





# average_ratings.loc[idx[['1Mmirg','tinderfire'],:],:]

# average_ratings.xs(0,labels=0)
# [[group1 in f1[1] for group1, group2 in average_ratings.index]]



# # Alternately, here's the syntax for making a pivot table:
# # pivot=pd.pivot_table(preferences, values='USER_RATING', index=['USER_NAME'],columns=['GAME_ID'],fill_value=0)
# # sparse_matrix=sparse.csc_matrix(pivot)
