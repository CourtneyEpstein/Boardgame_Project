from flask import Flask,render_template,jsonify,request
from app import app
import pymysql as mdb
import sys
sys.path.append("../recommend/")
# import recommend

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
 
@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    # print ret_data
    # PYTHON MAGIC
    # recommendations=recommend.make_recommendation(ret_data['value'])
    # recommendations=ret_data.values()
    # print recommendations
    recommendations=[2,4,24]
    with db:
        cur = db.cursor()
        # print "LOOK AT ME!!!!!!!",ret_data['value']
        cur.execute("SELECT GAME_NAME,URL,IMAGE,DESCRIPTION,YEAR FROM Basics WHERE GAME_ID IN ("+"'" + "','".join(str(rec) for rec in recommendations) +"');")
        query_results = cur.fetchall()
    # print 'TRY THIS!!!!!!!!',query_results
    games = []
    for result in query_results:
        games.append(dict(game=result[0], url=result[1], image=result[2], description=result[3], year=result[4]))
    # print 'LOOOK!!',games
    return jsonify(dict(games=games))

