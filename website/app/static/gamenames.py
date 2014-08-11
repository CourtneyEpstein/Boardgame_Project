import pymysql as mdb
import io, json

db = mdb.connect(user="root", passwd="mandrake", host="localhost", db="boardgamegeek", charset='utf8')


with db:
    cur = db.cursor()
    cur.execute('SELECT GAME_ID,GAME_NAME FROM Games ORDER BY GAME_NAME;')
    query_results = cur.fetchall()
games = dict()
for result in query_results:
    games[result[0]]=result[1]
# print games


# with open('all_game_names.txt', 'w') as outfile:
#   json.dump(games, outfile, ensure_ascii=False)

with io.open('all_game_names.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(games, ensure_ascii=False)))