from bs4 import BeautifulSoup
import os 
import re
import pandas as pd
import numpy as np

def function(name):
    return int(re.findall('page(.+)\.',name)[0])

def get_names(gameid):
    folder='boardgamegeekdata/game{0}/'.format(gameid)
    filenames=sorted(os.listdir(folder),key=function)
    return folder,filenames

def plothistogram(xmin,xmax,values,axis,color='Red',nbin=40,normalize=False):
    n,binEdges=np.histogram(values,bins=nbin,range=(xmin,xmax))
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    width=binEdges[1:]-binEdges[:-1]
    if(normalize==True):
        norm=[float(n[i])/float(sum(n)) for i in range(len(n))]
        axis.bar(bincenters,norm,width=width,facecolor=color)
    else:
        axis.bar(bincenters,n,width=width,facecolor=color)
    return bincenters,n

# gameid=40834
# 36218
# gameid=9209
gameid=13
folder,filenames=get_names(gameid)
get_names(gameid)

for i,filename in enumerate(filenames):
# for i,filename in enumerate([filenames[0],filenames[1]]):
    soup=BeautifulSoup(open(folder+filename), "xml")
    comments=soup.find_all('comment')
    if(i==0):
        boardgame_name=soup.find("name").attrs['value']
        boardgame_id=soup.find(type="boardgame")['id']
        boardgame_family_name=soup.find(type="boardgamefamily")['value']
        boardgame_family_id=soup.find(type="boardgamefamily")['id']
        boardgame_year=int(soup.yearpublished['value'])
        boardgame_min_player=int(soup.minplayers['value'])
        boardgame_max_player=int(soup.maxplayers['value'])
        boardgame_play_time=int(soup.playingtime['value'])
        boardgame_image=soup.image.text
        boardgame_mechanic=[ mechanic.attrs['value'] for mechanic in soup.find_all('link',type='boardgamemechanic')]
        boardgame_weight=float(soup.averageweight['value'])
        user_name=[comment.attrs['username'] for comment in comments]
        user_rating=[float(comment.attrs['rating']) for comment in comments]
    else:
        [user_name.append(comment.attrs['username']) for comment in comments]
        [user_rating.append(float(comment.attrs['rating'])) for comment in comments]
        print len(user_rating)

user=pd.Series(data=user_rating,index=user_name)
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


fig=plt.figure()
xmin=0.5
xmax=10.5
ymin=0
ymax=16000

ax = fig.add_subplot(111)
plt.xlabel('User Rating',size=16)
plt.ylabel('N',size=16)
plt.xticks(np.arange(1, 11, 1))
ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)
ax.annotate('{0}'.format(boardgame_name), xy=(0.05, 0.85), xycoords="axes fraction",size=20)
user.hist(bins=range(12),ax=ax,align='left',grid=False)

fig.savefig('game{0}.eps'.format(gameid))


