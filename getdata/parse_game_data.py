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
f=open('mysql_password.txt','r')
mysqlpass=f.read().split('\n')
f.close()
con = mdb.connect('localhost', mysqlpass[0], mysqlpass[1], 'boardgamegeek',charset='utf8')

# for ii,gameid in enumerate(all_gameid[0:1000]):
# for ii,gameid in enumerate(all_gameid[1000:5000]):
for ii,gameid in enumerate(all_gameid[8657:]):
# for gameid in all_gameid[0:1]:
    print ii,gameid
    folder,filenames=get_names(gameid)
    '''Open connection to MySQL'''  
    with con:
        cur = con.cursor()
        '''Only create a new table for the first entry'''
        if(gameid == 1):
            # MAKE TABLE THAT CONTAINS USER PREFERENCES
            cur.execute('DROP TABLE IF EXISTS Preferences')
            cur.execute("CREATE TABLE `Preferences`(\
            `USER_NAME` CHAR(20),\
            `GAME_ID` INT(6),\
            `GAME_NAME` CHAR(100),\
            `USER_RATING` DECIMAL(8,5)\
            );")
            # MAKE TABLE THAT CONTAINS BOARDGAME ATTRIBUTES
            '''Make list of column names'''
            all_colNameFormat = [\
                ['GAME_ID','INT(6)'],
                ['GAME_NAME','CHAR(100)'],
                ['PLAYING_TIME','DECIMAL(10,1)'],
                ['GAME_WEIGHT','DECIMAL(10,5)'],
                ['MIN_PLAYER_MANUFACTURER','INT(2)'],
                ['MAX_PLAYER_MANUFACTURER','INT(2)']
                ]
            for i in range(1,31):
                all_colNameFormat.append(["POLL_BEST_NUM_PLAYERS={0}".format(i),'DECIMAL(6,0)'])
                all_colNameFormat.append(["POLL_OK_NUM_PLAYERS={0}".format(i),'DECIMAL(6,0)'])
                all_colNameFormat.append(["POLL_BAD_NUM_PLAYERS={0}".format(i),'DECIMAL(6,0)'])
            f=open('board_game_categories.txt','r')
            category_names=f.read()
            f.close()
            all_colNameFormat.extend([category,'BOOLEAN'] for category in category_names.split('\n'))
            f=open('board_game_mechanics.txt','r')
            mechanic_names=f.read()
            f.close()
            all_colNameFormat.extend([mechanic,'BOOLEAN'] for mechanic in mechanic_names.split('\n'))
            all_colNameFormat=np.array(all_colNameFormat)
            cur.execute('DROP TABLE IF EXISTS Games')
            create_games_table_cmd = 'CREATE TABLE `Games` ( '
            for col_name,col_format in all_colNameFormat:
                create_games_table_cmd=create_games_table_cmd+'`{0}` {1},'.format(col_name,col_format)
            create_games_table_cmd=create_games_table_cmd+'PRIMARY KEY (`GAME_ID`));'
            cur.execute(create_games_table_cmd)
            # MAKE TABLE THAT CONTAINS BOARDGAME INFORMATION FOR DISPLAY ON WEBSITE
            cur.execute('DROP TABLE IF EXISTS Basics')
            cur.execute("CREATE TABLE `Basics`(\
            `GAME_ID` INT(6) NOT NULL PRIMARY KEY,\
            `GAME_NAME` CHAR(100),\
            `YEAR` INT(4),\
            `URL` CHAR(45),\
            `IMAGE` CHAR(70),\
            `DESCRIPTION` TEXT \
            );")

            all_colNames=[name for name,junk in all_colNameFormat]

        for i,filename in enumerate(filenames):
        # for i,filename in enumerate([filenames[0]]):
            '''Read in each file and parse as .xml with BeautifulSoup'''
            soup=BeautifulSoup(open(folder+filename), "xml")
            comments=soup.find_all('comment')
            expansions=soup.find_all(type="boardgameexpansion")
            if(i==0):
                '''Store information about boardgames in dictionary bg'''
                bg={name:None for name in all_colNames }

                colNames=['GAME_ID','GAME_NAME','MIN_PLAYER_MANUFACTURER','MAX_PLAYER_MANUFACTURER','GAME_WEIGHT','PLAYING_TIME']
                bg['GAME_ID']=soup.find(type="boardgame")['id']
                bg['GAME_NAME']=soup.find("name",type="primary").attrs['value']
                if(bg['GAME_ID']=='10405'):
                    print "in if"
                    bg['GAME_NAME']=soup.find("name",type="alternate").attrs['value']
                try:
                    bg['MIN_PLAYER_MANUFACTURER']=soup.minplayers['value']
                except:
                    continue
                try:
                    bg['MAX_PLAYER_MANUFACTURER']=soup.maxplayers['value']
                except:
                    continue
                try:
                    bg['GAME_WEIGHT']=soup.averageweight['value']
                except:
                    continue
                try:
                    bg['PLAYING_TIME']=soup.playingtime['value']
                    if(bg['PLAYING_TIME']==0):
                        bg['PLAYING_TIME']=None
                except:
                    continue

                # 30 looks like the maximum number of players 
                for nplayers in range(1,min(31,int(bg['MAX_PLAYER_MANUFACTURER'])+1)):
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
                
                boardgame_category=[ 'CATEGORY: '+category.attrs['value'] for category in soup.find_all('link',type='boardgamecategory')]
                for cat in boardgame_category:
                    colNames.append(cat)
                    bg[(cat)]='1'
                boardgame_mechanic=[ 'MECHANIC: '+mechanic.attrs['value'] for mechanic in soup.find_all('link',type='boardgamemechanic')]
                for mech in boardgame_mechanic:
                    colNames.append(mech)
                    bg[mech]='1'

                # insert_games_cmd='INSERT INTO Games(`'+ '`,`'.join(colNames) +'`) VALUES('+','.join([bg[cn] for cn in colNames])+');'
                # cur.execute(insert_games_cmd)
                # cur.execute('INSERT INTO Games(%s) VALUES(%s) ',('`'+'`,`'.join(colNames)+'`',[bg[cn] for cn in colNames])))
                # values=[bg[cn] for cn in all_colNames]
                # format_string=','.join(['%s']*len(colNames))
                format_string=','.join(['%s']*len(all_colNames))

                cur.execute('INSERT INTO Games VALUES('+format_string+')',(bg[cn] for cn in all_colNames))
                # cur.execute('INSERT INTO Games(%s) VALUES(%s)',('`'+'`,`'.join(colNames)+'`',bg[cn]))


                '''The table Basics is mostly intended for displaying information on the website.
                Define and execute MySQL command here to fill the Basics table.'''
                try:
                    bg['DESCRIPTION']=soup.description.text
                    # bg['DESCRIPTION']=mdb.escape_string(soup.description.text)
                except:
                    bg['DESCRIPTION']='NULL'
                try:
                    bg['IMAGE']=soup.image.text
                except:
                    bg['IMAGE']='NULL'
                bg['URL']='http://boardgamegeek.com/boardgame/{0}'.format(gameid)
                try:
                    bg['YEAR']=soup.yearpublished['value']
                except:
                    bg['YEAR']='NULL'
                # insert_basics_cmd = 'INSERT INTO Basics VALUES('+",".join([bg['GAME_ID'],bg['GAME_NAME'],bg['YEAR'],"'"+bg['URL']+"'","'"+bg['IMAGE']+"'","'''"+bg['DESCRIPTION']+"'''"]) +');'
                # cur.execute(insert_basics_cmd)
                cur.execute('INSERT INTO Basics VALUES(%s,%s,%s,%s,%s,%s)',(bg['GAME_ID'],bg['GAME_NAME'],bg['YEAR'],bg['URL'],bg['IMAGE'],bg['DESCRIPTION']))
            
            # '''For each comment, extract that username and rating.
            # Define and execute MySQL command here to fill the Preferences table.'''
            for comment in comments:
                # insert_preferences_cmd = 'INSERT INTO Preferences VALUES('+','.join(["'"+comment.attrs['username']+"'",bg['GAME_ID'],bg['GAME_NAME'],comment.attrs['rating']]) +');'
                # cur.execute(insert_preferences_cmd)
                cur.execute('INSERT INTO Preferences VALUES(%s,%s,%s,%s);',(comment.attrs['username'],bg['GAME_ID'],bg['GAME_NAME'],comment.attrs['rating']))
