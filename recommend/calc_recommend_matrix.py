import numpy as np
import pymysql as mdb
import cPickle as pickle
import sys
import pandas as pd
import scipy.sparse as sparse
import math
from useful import *

con=connect_to_MySQL()

try:
    preferences
except:
    print "Reading from MySQL..."
    preferences=pd.io.sql.read_sql('SELECT P.USER_NAME,P.GAME_ID,P.USER_RATING FROM Preferences AS P LEFT JOIN (SELECT USER_NAME,COUNT(DISTINCT GAME_ID) AS CNT FROM Preferences GROUP BY USER_NAME) as TMP ON P.USER_NAME=TMP.USER_NAME WHERE TMP.CNT BETWEEN 10 AND 100;',con)
    print "Done reading from MySQL."

# preferences=pd.io.sql.read_sql('SELECT * FROM Preferences LIMIT 100000;',con,coerce_float=True)

average_ratings=preferences.groupby(['USER_NAME','GAME_ID']).mean()
'''Define the translation between
user=True: row # (index) and user name (value); OR
game=True: column # (index) and game id (value)'''
translate=translator(average_ratings)
'''Use the pandas multiindex to define the coordinates of the array'''
levels_user=list(average_ratings.index.levels[0])
levels_game=list(average_ratings.index.levels[1])
labels_user=list(average_ratings.index.labels[0])
labels_game=list(average_ratings.index.labels[1])
''' and the values, averaged if there are multiple ratings by the same user per game'''
data_rating=average_ratings.ix[:,0].values
'''This is a matrix with users on the rows and games on the columns'''
ratings=sparse.coo_matrix((data_rating,(labels_user,labels_game)),shape=(len(levels_user),len(levels_game)))
'''Once a matrix has been constructed, convert to CSR or CSC format for fast arithmetic and matrix vector operations'''
userXgame=ratings.tocsc()
gameXgame=(userXgame.T).dot(userXgame)
'''The sum of squares is the entry along the diagonal
Cosine similarity is divided by the magnitude of the vector
To get the magnitude, take the sqrt of the dot product (i.e. the diagonal)
Compute this for every entry on the diagonal'''
diagonals = [1/math.sqrt(gameXgame[i,i]) for i in range(len(levels_game))]
'''Convert this to a sparse matrix'''
diag_norm = sparse.diags(diagonals,offsets=0)
cosine_similarity_gameXgame = diag_norm.dot(gameXgame).dot(diag_norm)

'''Output resulting similarity matrix to file'''
pickle.dump(translate,open( "translator.pkl", "wb" ))
pickle.dump(cosine_similarity_gameXgame,open( "game_recommendation_matrix_cosine.pkl", "wb" ))





# Alternately, here's the syntax for making a pivot table:
# pivot=pd.pivot_table(preferences, values='USER_RATING', index=['USER_NAME'],columns=['GAME_ID'],fill_value=0)
# sparse_matrix=sparse.csc_matrix(pivot)
