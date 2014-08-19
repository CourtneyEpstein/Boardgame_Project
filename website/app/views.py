from flask import Flask,render_template,jsonify,request
from app import app
import pymysql as mdb
from  sys import path

path.append("/Users/athena/Insight/Boardgame_Project/final/recommend/")
import recommend

db = mdb.connect(user="root", passwd="mandrake", host="localhost", db="boardgamegeek", charset='utf8')

@app.route('/')
@app.route('/index')

# def index():
#     return render_template("index.html",
#         title = 'Home', user = { 'nickname': 'Courtney' },
#         )

# @app.route('/db')
# def cities_page():
#     with db: 
#         cur = db.cursor()
#         cur.execute("SELECT Name FROM city LIMIT 15;")
#         query_results = cur.fetchall()
#     cities = ""
#     for result in query_results:
#         cities += result[0]
#         cities += "<br>"
#     return cities

# @app.route("/db_fancy")
# def cities_page_fancy():
#     with db:
#         cur = db.cursor()
#         cur.execute("SELECT Name, CountryCode, \
#             Population FROM city ORDER BY Population LIMIT 15;")

#         query_results = cur.fetchall()
#     cities = []
#     for result in query_results:
#         cities.append(dict(name=result[0], country=result[1], population=result[2]))
#     return render_template('cities.html', cities=cities) 

@app.route("/jquery")
def index_jquery():
    return render_template('boardgame.html')

@app.route("/db_json")
def games_json():
    with db:
        cur = db.cursor()
        cur.execute("SELECT GAME_NAME, URL, IMAGE  FROM Basics LIMIT 15;")
        query_results = cur.fetchall()
    games = []
    for result in query_results:
        games.append(dict(game=result[0], url=result[1], image=result[2]))
    return jsonify(dict(games=games))


# @app.before_request
# def before_request():
#     if request.path != '/':
#         if request.headers['content-type'].find('application/json'):
#             return 'Unsupported Media Type', 415
 
# # @app.route('/')
# # def index():
# #     return render_template('index1.html')
 
# @app.route('/echo/', methods=['GET'])
@app.route("/get_games/")
def get_games():
    ret_data = {"game_name": request.args.get('gamename'),"playingtime":request.args.get('playingtime'),"numplayers":request.args.get('numplayers'),"stars":request.args.get('stars')}
    print ret_data
    # PYTHON MAGIC
    get_recs=recommend.rec_engine()
    get_recs.add_input_game(ret_data["game_name"],8)
    # # get_recs.add_input_game('The Settlers of Catan',5)
    get_recs.add_input_time(ret_data["playingtime"])
    get_recs.add_input_num_players(ret_data["numplayers"])
    recommendations = get_recs.recommend()
    # recommendations=[13,148228,34635,20,70,90]
    with db:
        cur = db.cursor()
        # print "LOOK AT ME!!!!!!!",ret_data['value']
        cur.execute("SELECT B.GAME_NAME,B.URL,B.IMAGE,B.DESCRIPTION,B.YEAR,G.PLAYING_TIME,G.MIN_PLAYER_MANUFACTURER,G.MAX_PLAYER_MANUFACTURER,G.GAME_WEIGHT,B.GAME_ID FROM Basics as B LEFT JOIN Games as G ON G.GAME_ID=B.GAME_ID WHERE B.GAME_ID IN ("+"'" + "','".join(str(rec) for rec in recommendations) +"');")
        query_results = cur.fetchall()
    # print 'TRY THIS!!!!!!!!',query_results
    games = []
    brains={1:'Easygoing Entertainment',2:'Satisfyingly Stimulating',3:'Approachably Arduous',4:'Thoroughly Thinky',5:'Brain Burning'}
    for result in query_results:
        if(1.0<=result[8]<1.5):
            game_weight=brains[1]
        elif(1.5<=result[8]<2.25):
            game_weight=brains[2]
        elif(2.25<=result[8]<2.75):
            game_weight=brains[3]
        elif(2.75<=result[8]<3.5):
            game_weight=brains[4]
        elif(3.5<=result[8]<=5):
            game_weight=brains[5]
        else:
            game_weight="Uncertain Brainpower Requirements"

        games.append(dict(game=result[0], url=result[1], image=result[2], description=result[3], year=result[4], playingtime=int(result[5]),min_players=result[6],max_players=result[7],game_weight=game_weight))
    # print 'LOOOK!!',games
    return jsonify(dict(games=games))

