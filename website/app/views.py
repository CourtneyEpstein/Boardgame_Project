from flask import Flask,render_template,jsonify
from app import app
import pymysql as mdb

db = mdb.connect(user="root", passwd="mandrake", host="localhost", db="boardgamegeek", charset='utf8')

@app.route('/')
@app.route('/index')

def index():
    return render_template("index.html",
        title = 'Home', user = { 'nickname': 'Courtney' },
        )

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

