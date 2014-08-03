import urllib2
from bs4 import BeautifulSoup,SoupStrainer
import os


def get_boardgamegeek_url(gameid,page):
    url='http://boardgamegeek.com/xmlapi2/thing?type=boardgame&ratingcomments=1&stats=1&id={0}&page={1}'.format(gameid,page)
    return urllib2.urlopen(url).read()


def main():
    # gameid=40834
    
    for gameid in range(87119,150000):
        skip=False
        page=1
        
        result=get_boardgamegeek_url(gameid,page)
        strainer=SoupStrainer("comments")
        try:
            n_comments=int(BeautifulSoup(result,"xml",parse_only=strainer).comments['totalitems'])
        except:
            skip=True
            print "skipping {0}".format(gameid)

        if not skip:
            n_pages=n_comments//100
            if n_comments % 100 != 0:
                n_pages+=1
            
            
            outfolder='/Users/athena/Insight/Boardgame_Project/getdata/boardgamegeekdata/game{0}'.format(gameid)
            if not os.path.exists(outfolder):
                os.mkdir(outfolder)    
            
            # for page in [1]:
            for page in range(1,n_pages+1):
                print '{0} of {1} pages of comments'.format(page,n_pages)
                if(page != 1):
                    result=get_boardgamegeek_url(gameid,page)
                outfile='game{0}_page{1}.xml'.format(gameid,page)
                # print outfile
                f=open(outfolder+'/'+outfile,'w')
                f.write(result)
                f.close()

    # Standard boilerplate to call the main() function to begin
    # the program.
if __name__ == '__main__':
    main()

