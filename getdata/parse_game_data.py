from bs4 import BeautifulSoup
import os 
import re
import numpy as np
import MySQLdb as mdb


def paginator(name):
    '''Used to numerically sort the filenames;
    uses a regular expression search to find the number of pages
    and converts it to an integer'''
    return int(re.findall('page(.+)\.',name)[0])

def get_names(gameid):
    '''For a given game id #, this function returns:
    (1) the absolute path of the folder where that game's data is located
    (2) the filenames for all of the pages pertaining to that game
    Remember: only 100 user comments/ratings returned per page by the boardgamegeek.com API
    '''
    folder=os.path.abspath('boardgamegeekdata/game{0}'.format(gameid))+'/'
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
    all_gameid=sorted([int(name[4:]) for name in contents if(name[0:4]=='game')])
    return all_gameid

all_gameid=get_viable_game_ids()

'''Define connection to the MySQL database, boardgamegeek'''
con = mdb.connect('localhost', 'root', 'mandrake', 'boardgamegeek')


# for gameid in all_gameid[0:5]:
for gameid in all_gameid[0:1]:
    print gameid
    folder,filenames=get_names(gameid)
    '''Store information about boardgames in dictionary bg'''    
    bg={}
    '''Open connection to MySQL'''  
    with con:
        cur = con.cursor()
        # if(gameid == 1):
            ## MAKE TABLE THAT CONTAINS USER PREFERENCES
            # cur.execute('DROP TABLE IF EXISTS Preferences')
            # cur.execute("CREATE TABLE `Preferences`(\
            # `USER_NAME` CHAR(20),\
            # `GAME_ID` INT(6),\
            # `GAME_NAME` CHAR(100),\
            # `USER_RATING` DECIMAL(5,2)\
            # ) DEFAULT CHARSET=utf8;")
            ## MAKE TABLE THAT CONTAINS BOARDGAME ATTRIBUTES
            # '''Make list of column names'''
            # all_colNames = [\
            #     ['BOARDGAME_ID','INT(6)'],
            #     ['BOARDGAME_NAME','CHAR(20)'],
            #     ['PLAYING_TIME','DECIMAL(10,1)'],
            #     ['BOARDGAME_WEIGHT','DECIMAL(10,5)'],
            #     ['MIN_PLAYER_MANUFACTURER','INT(2)'],
            #     ['MAX_PLAYER_MANUFACTURER','INT(2)']
            #     ]
            # print len(all_colNames)
            # for i in range(1,31):
            #     all_colNames.append(["POLL_BEST_NUM_PLAYERS={0}".format(i),'DECIMAL(6,0)'])
            #     all_colNames.append(["POLL_OK_NUM_PLAYERS={0}".format(i),'DECIMAL(6,0)'])
            #     all_colNames.append(["POLL_BAD_NUM_PLAYERS={0}".format(i),'DECIMAL(6,0)'])
            # print len(all_colNames)
            # f=open('board_game_categories.txt','r')
            # category_names=f.read()
            # f.close()
            # all_colNames.extend([category,'BOOLEAN'] for category in category_names.split('\n'))
            # print len(all_colNames)
            # f=open('board_game_mechanics.txt','r')
            # mechanic_names=f.read()
            # f.close()
            # all_colNames.extend([mechanic,'BOOLEAN'] for mechanic in mechanic_names.split('\n'))
            # print len(all_colNames)
            # all_colNames=np.array(all_colNames)
            # print all_colNames
            # cur.execute('DROP TABLE IF EXISTS Games')
            # create_games_table_cmd = 'CREATE TABLE `Games` ( '
            # for col_name,col_format in all_colNames:
            #     create_games_table_cmd=create_games_table_cmd+'`{0}` {1},'.format(col_name,col_format)
            # create_games_table_cmd=create_games_table_cmd+'PRIMARY KEY (`BOARDGAME_ID`)) DEFAULT CHARSET=utf8;;'
            # print create_games_table_cmd
            # cur.execute(create_games_table_cmd)
            ## MAKE TABLE THAT CONTAINS BOARDGAME INFORMATION FOR DISPLAY ON WEBSITE
            # cur.execute('DROP TABLE IF EXISTS Basics')
            # cur.execute("CREATE TABLE `Basics`(\
            # `GAME_ID` INT(6) NOT NULL PRIMARY KEY,\
            # `GAME_NAME` CHAR(100),\
            # `YEAR` INT(4),\
            # `URL` CHAR(45),\
            # `IMAGE` CHAR(70),\
            # `DESCRIPTION` TEXT \
            # ) DEFAULT CHARSET=utf8;")
    
        # for i,filename in enumerate(filenames):
        # for i,filename in enumerate([filenames[0],filenames[1]]):
        for i,filename in enumerate([filenames[0]]):
            soup=BeautifulSoup(open(folder+filename), "xml")
            comments=soup.find_all('comment')
            categories=soup.find_all(type="boardgamecategory")
            mechanics=soup.find_all(type="boardgamemechanic")
            expansions=soup.find_all(type="boardgameexpansion")
            if(i==0):
                colNames=['BOARDGAME_NAME','BOARDGAME_ID','MIN_PLAYER_MANUFACTURER','MAX_PLAYER_MANUFACTURER','BOARDGAME_WEIGHT']
                bg['BOARDGAME_NAME']         =soup.find("name",type="primary").attrs['value']
                bg['BOARDGAME_ID']           =soup.find(type="boardgame")['id']
                bg['MIN_PLAYER_MANUFACTURER']=soup.minplayers['value']
                bg['MAX_PLAYER_MANUFACTURER']=soup.maxplayers['value']
                bg['BOARDGAME_WEIGHT']       =soup.averageweight['value']
                # 30 looks like the maximum number of players 
                for nplayers in range(int(bg['MIN_PLAYER_MANUFACTURER']),min(31,int(bg['MAX_PLAYER_MANUFACTURER'])+1)):
                    poll_result=soup.find("results",numplayers=nplayers)
                    try:
                        best="POLL_BEST_NUM_PLAYERS={0}".format(nplayers)
                        ok="POLL_OK_NUM_PLAYERS={0}".format(nplayers)
                        bad="POLL_BAD_NUM_PLAYERS={0}".format(nplayers)
                        bg[best],bg[ok],bg[bad]=[child['numvotes'] for child in poll_result.findChildren()]
                        colNames.extend([best,ok,bad])
                    except:
                        continue
                #Num_players
                #Proposal: Weight "best" by 
                # Ages
                # if less than half of the people think that the maximimum age
                # is over 21, then take the mode age <21 as the maximum age
                bg['PLAYING_TIME']=soup.playingtime['value']
                if(bg['PLAYING_TIME']==0):
                    bg['PLAYING_TIME']=None
                
        #     #     boardgame_mechanic=[ mechanic.attrs['value'] for mechanic in soup.find_all('link',type='boardgamemechanic')]

                # print bg

                '''The table Basics is mostly intended for displaying information on the website.
                Define and execute MySQL command here to fill the Basics table.'''
                # bg['DESCRIPTION']=soup.description.text
                # bg['IMAGE']=soup.image.text
                # bg['URL']='http://boardgamegeek.com/boardgame/{0}'.format(gameid)
                # bg['YEAR']=soup.yearpublished['value']
                # insert_basics_cmd = 'INSERT INTO Basics VALUES('+",".join([bg['BOARDGAME_ID'],"'"+bg['BOARDGAME_NAME']+"'",bg['YEAR'],"'"+bg['URL']+"'","'"+bg['IMAGE']+"'",'"'+bg['DESCRIPTION']+'"']) +');'
                # cur.execute(insert_basics_cmd)
            
            '''For each comment, extract that username and rating.
            Define and execute MySQL command here to fill the Preferences table.'''
            # for comment in comments:
                # insert_preferences_cmd = 'INSERT INTO Preferences VALUES('+','.join(["'"+comment.attrs['username']+"'",bg['BOARDGAME_ID'],"'"+bg['BOARDGAME_NAME']+"'",comment.attrs['rating']]) +');'
                # cur.execute(insert_preferences_cmd)





# 
# formatStrings = []
# values = []

# for colName, value in bg.items():
#     if not value == None:
#         colNames.append(colName)
#         values.append(value)
#         formatStrings.append('%s')

# insertStatement = "INSERT INTO {0}({1}) VALUES({2})".format(
#     'Preferences', 
#     ', '.join(colNames), 
#     ', '.join(values))


# with con:
    # c.execute("INSERT INTO preferences (USER_NAME) VALUES ('GARY')")




    #     user_name=[comment.attrs['username'] for comment in comments]
    #     user_rating=[float(comment.attrs['rating']) for comment in comments]
    # else:
    #     [user_name.append(comment.attrs['username']) for comment in comments]
    #     [user_rating.append(float(comment.attrs['rating'])) for comment in comments]
    #     print len(user_rating)

# user=pd.Series(data=user_rating,index=user_name)
# count,division = np.histogram(user)

# print boardgame_name
# print boardgame_id
# print boardgame_family_name
# print boardgame_family_id
# print boardgame_min_player,boardgame_max_player
# print boardgame_play_time
# print boardgame_year
# print boardgame_image
# print boardgame_mechanic
# print boardgame_weight
# print users

