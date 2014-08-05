from bs4 import BeautifulSoup
import os 
import re
# import pandas as pd
import numpy as np
import MySQLdb as mdb


def paginator(name):
    return int(re.findall('page(.+)\.',name)[0])

def get_names(gameid):
    folder=os.path.abspath('boardgamegeekdata/game{0}/'.format(gameid))
    if os.path.exists(folder):
        filenames=sorted(os.listdir(folder),key=paginator)
    else:
        filenames=None
    return folder,filenames

def get_viable_game_ids():
    '''Searches the folder containing all of the data scraped from boardgamegeek.com
    '''
    abspath=os.path.abspath('boardgamegeekdata')
    contents=os.listdir(abspath)
    all_gameid=[int(name[4:]) for name in contents if(name[0:4]=='game')]
    return all_gameid

all_gameid=get_viable_game_ids()


# con = mdb.connect('localhost', 'root', 'mandrake', 'boardgamegeek')


# # gameid=40834
# # 36218
# # gameid=9209
# # gameid=34635
# # for gameid in range(1,21):
# for gameid in range(1,5):
#     print gameid
#     folder,filenames=get_names(gameid)
#     print folder, filenames
#     # get_names(gameid)
    
#     bg={}
    
#     with con:
#         cur = con.cursor()
#         # if(gameid == 1):
#             ## MAKE TABLE THAT CONTAINS USER PREFERENCES
#             # cur.execute('DROP TABLE IF EXISTS Preferences')
#             # cur.execute("CREATE TABLE `Preferences`(\
#             # `USER_NAME` CHAR(20),\
#             # `BOARDGAME_ID` INT(6),\
#             # `BOARDGAME_NAME` CHAR(100),\
#             # `USER_RATING` DECIMAL(5,2)\
#             # ) DEFAULT CHARSET=utf8;")
#             ## MAKE TABLE THAT CONTAINS BOARDGAME ATTRIBUTES
#             # cur.execute('DROP TABLE IF EXISTS Games')
#             # cur.execute("CREATE TABLE `Games`(\
#             # `BOARDGAME_ID` INT(6),\
#             # `BOARDGAME_NAME` CHAR(100),\
#             # `USER_RATING` DECIMAL(5,2),\
#             # PRIMARY KEY (`BOARDGAME_ID`),
#             # ) DEFAULT CHARSET=utf8;")
#             ## MAKE TABLE THAT CONTAINS BOARDGAME INFORMATION FOR DISPLAY ON WEBSITE
#             # cur.execute('DROP TABLE IF EXISTS Basics')
#             # cur.execute("CREATE TABLE `Basics`(\
#             # `BOARDGAME_ID` INT(6),\
#             # `BOARDGAME_NAME` CHAR(100),\
#             # # `USER_RATING` DECIMAL(5,2)\
#             # ) DEFAULT CHARSET=utf8;")
    
#         for i,filename in enumerate(filenames):
#             # for i,filename in enumerate([filenames[0],filenames[1]]):
#         # for i,filename in enumerate([filenames[0]]):
#             soup=BeautifulSoup(open(folder+filename), "xml")
#             comments=soup.find_all('comment')
#             # categories=soup.find_all(type="boardgamecategory")
#             #     # mechanics=soup.find_all(type="boardgamemechanic")
#             #     # expansions=soup.find_all(type="boardgameexpansion")
#             if(i==0):
#                 bg['BOARDGAME_NAME']=soup.find("name",type="primary").attrs['value']
#                 bg['BOARDGAME_ID']=soup.find(type="boardgame")['id']
#         #         # bg['MIN_PLAYER_MANUFACTURER']=int(soup.minplayers['value'])
#         #         # bg['MAX_PLAYER_MANUFACTURER']=int(soup.maxplayers['value'])
#         #     #     # 30 looks like the maximum number of players 
#         #     #     num_players={}
#         #         # for nplayers in range(boardgame_min_player,boardgame_max_player+1):
#         #     #         poll_result=soup.find("results",numplayers=nplayers)
#         #     #         votes=[int(child['numvotes']) for child in poll_result.findChildren()]
#         #     #         num_players[nplayers]=[float(vote)/sum(votes) for vote in votes]
#         #     #     print num_players
#         #         #Num_players
#         #         #Proposal: Weight "best" by 
#         #         # Ages
#         #         # if less than half of the people think that the maximimum age
#         #         # is over 21, then take the mode age <21 as the maximum age
#         #     #     boardgame_play_time=int(soup.playingtime['value'])
#         #         # For website display only
#                 bg['DESCRIPTION']=soup.description.text
#                 bg['IMAGE']=soup.image.text
#                 bg['YEAR']=soup.yearpublished['value']
#                 insert_basics_cmd = 'INSERT INTO Basics VALUES('+",".join([bg['BOARDGAME_ID'],"'"+bg['BOARDGAME_NAME']+"'",bg['YEAR'],"'"+bg['IMAGE']+"'","'"+bg['DESCRIPTION']+"'"]) +');'
#                 print insert_basics_cmd

#         #     #     boardgame_mechanic=[ mechanic.attrs['value'] for mechanic in soup.find_all('link',type='boardgamemechanic')]
#         #     #     boardgame_weight=float(soup.averageweight['value'])
            
#             # for comment in comments:
#             #     insert_preferences_cmd = 'INSERT INTO Preferences VALUES('+','.join(["'"+comment.attrs['username']+"'",bg['BOARDGAME_ID'],"'"+bg['BOARDGAME_NAME']+"'",comment.attrs['rating']]) +');'
#             #     # print insert_preferences_cmd
#             #     cur.execute(insert_preferences_cmd)





# # colNames = []
# # formatStrings = []
# # values = []

# # for colName, value in bg.items():
# #     if not value == None:
# #         colNames.append(colName)
# #         values.append(value)
# #         formatStrings.append('%s')

# # insertStatement = "INSERT INTO {0}({1}) VALUES({2})".format(
# #     'Preferences', 
# #     ', '.join(colNames), 
# #     ', '.join(values))


# # with con:
#     # c.execute("INSERT INTO preferences (USER_NAME) VALUES ('GARY')")




#     #     user_name=[comment.attrs['username'] for comment in comments]
#     #     user_rating=[float(comment.attrs['rating']) for comment in comments]
#     # else:
#     #     [user_name.append(comment.attrs['username']) for comment in comments]
#     #     [user_rating.append(float(comment.attrs['rating'])) for comment in comments]
#     #     print len(user_rating)

# # user=pd.Series(data=user_rating,index=user_name)
# # count,division = np.histogram(user)

# # print boardgame_name
# # print boardgame_id
# # print boardgame_family_name
# # print boardgame_family_id
# # print boardgame_min_player,boardgame_max_player
# # print boardgame_play_time
# # print boardgame_year
# # print boardgame_image
# # print boardgame_mechanic
# # print boardgame_weight
# # print users

