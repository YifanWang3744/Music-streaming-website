#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from re import I
import flask
from numpy import empty
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import datetime
from random import randint
# from web_scraper import *
# import numpy as np

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.211.155.104/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@35.211.155.104/proj1part2"
#
DATABASEURI = "postgresql://ap4142:2688@35.211.155.104/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  # cursor = g.conn.execute("SELECT s_name FROM Songs")
  # names = []
  # for result in cursor:
  #   names.append(result['s_name'])  # can also be accessed using result[0]
  # cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  # context = dict(data=names)
  if request.cookies.get('uid'):
    logged_in_uid = request.cookies.get('uid')
    cursor = g.conn.execute("select A.artist_id, A.artist_name from artist A where A.artist_id not in (select followed_by.artist_id from followed_by where followed_by.user_id={}) ORDER BY RANDOM() limit 5".format(logged_in_uid))
    artists = []
    for res in cursor:
            artists.append({
                "artist_id": res["artist_id"],
                "artist_name": res["artist_name"]
            })

    cursor = g.conn.execute("select A.song_id, A.name from song A ORDER BY RANDOM() limit 5")
    songs = []
    for res in cursor:
            songs.append({
                "song_id": res["song_id"],
                "name": res["name"]
            })

  else:
    cursor = g.conn.execute("select A.artist_id, A.artist_name from artist A ORDER BY RANDOM() limit 5")
    artists = []
    for res in cursor:
            artists.append({
                "artist_id": res["artist_id"],
                "artist_name": res["artist_name"]
            })

    cursor = g.conn.execute("select A.song_id, A.name from song A ORDER BY RANDOM() limit 5")
    songs = []
    for res in cursor:
            songs.append({
                "song_id": res["song_id"],
                "name": res["name"]
            })

  
  context = {
    "songs": songs,
    "artists": artists
  }
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute("INSERT INTO test(name) VALUES ('{}');".format(name))
    return redirect('/')


@app.route('/search', methods=['POST'])
def search():
    query = request.form["query"]
    if query == "":
        context = {"error_message": "No results found."}
        return render_template("search.html", **context)

    query = query.strip().lower()
    context = {}

    d = {"query": "%" + query + "%"}
    # Find Songs
    context["songs_found"] = []
    cursor = g.conn.execute(text("""SELECT song_id, name, rel_time, album_id FROM song WHERE name ILIKE :query"""), **d)
    for res in cursor:
        context["songs_found"].append({
            "song_id": res["song_id"],
            "rel_time": res["rel_time"],
            "name": res["name"],
            "album_id": res["album_id"]
        })

    # Find record
    context["record_found"] = []
    cursor = g.conn.execute(text("""SELECT record_id, name FROM record WHERE name ILIKE :query"""), **d)
    for res in cursor:
        context["record_found"].append({
            "record_id": res["record_id"],
            "name": res["name"]
        })

    # Find Albums
    context["albums_found"] = []
    cursor = g.conn.execute(text("""SELECT album_id, album_name, release_time FROM album WHERE album_name ILIKE :query"""), **d)
    for res in cursor:
        context["albums_found"].append({
            "album_id": res["album_id"],
            "album_name": res["album_name"],
            "release_time": res["release_time"]
        })

    # Find Artists
    context["artists_found"] = []
    cursor = g.conn.execute(text("""SELECT artist_id, artist_name, age FROM artist WHERE artist_name ILIKE :query"""), **d)
    for res in cursor:
        context["artists_found"].append({
            "artist_id": res["artist_id"],
            "artist_name": res["artist_name"],
            "age": res["age"]
        })

    # # Find Users
    # context["users_found"] = []
    # cursor = g.conn.execute(text("""SELECT user_id, name FROM users WHERE name ILIKE :query"""), **d)
    # for res in cursor:
    #     context["users_found"].append({
    #         "user_id": res["user_id"],
    #         "name": res["name"]
    #     })

    # Find Playlists
    context["playlists_found"] = []
    cursor = g.conn.execute(text("""SELECT playlist_id, name FROM playlist_createdby WHERE name ILIKE :query"""), **d)
    for res in cursor:
        context["playlists_found"].append({
            "playlist_id": res["playlist_id"],
            "name": res["name"]
        })
    if context["songs_found"] == [] and context["record_found"] == [] and context["albums_found"] == [] and context["artists_found"] == [] and context["playlists_found"] == []:
        context = {"error_message": "No results found."}
        return render_template("search.html", **context)
    else:
        return render_template("search.html", **context)

@app.route('/record/<record_id>')
def record(record_id):
    cursor = g.conn.execute("SELECT * FROM record WHERE record_id={}".format(record_id))
    record = cursor.fetchone()

    name, record_id = record["name"], record["record_id"]
    cursor = g.conn.execute("SELECT R.album_id, R.album_name FROM album R INNER JOIN owned_by O on R.album_id = O.album_id WHERE O.record_id={}".format(record_id))
    albums = []
    for res in cursor:
        albums.append( {
            "album_id": res["album_id"],
            "name": res["album_name"]
        })

    context = {
        "record_id": record_id,
        "name": name,
        "album_list": albums
    }

    return render_template("label.html", **context)

@app.route('/song/<song_id>')
def song(song_id):
    cursor = g.conn.execute("SELECT * FROM song WHERE song_id={}".format(song_id))
    song = cursor.fetchone()

    name, rel_time, album_id = song["name"], song["rel_time"], song["album_id"]
    cursor = g.conn.execute("SELECT A.artist_name, A.artist_id FROM song S, artist_of O, artist A where S.album_id=O.album_id and A.artist_id=O.artist_id and S.album_id={}".format(album_id))
    artist = cursor.fetchone()
    artist_id = artist["artist_id"]
    artist_name = artist["artist_name"]
    cursor = g.conn.execute("select album_name from album where album_id={}".format(album_id))
    album_name = cursor.fetchone()["album_name"]

    if request.cookies.get('uid'):
        logged_in_uid = request.cookies.get('uid')
        cursor = g.conn.execute("SELECT playlist_id, name from playlist_createdby where creator_user_id = {}".format(logged_in_uid))
        pl = []
        for res in cursor:
            pl.append( {
                "playlist_id": res["playlist_id"],
                "playlist_name": res["name"]
            })
    else:
        return redirect("/login")

    context = {
        "rel_time": rel_time,
        "name": name,
        "album_id": album_id,
        "artist_name": artist_name,
        "artist_id": artist_id,
        "album_name": album_name,
        "playlists": pl,
        "song_id": song_id
    }

    return render_template("song.html", **context)

@app.route('/album/<album_id>')
def album(album_id):
    cursor = g.conn.execute("SELECT * FROM album WHERE album_id={}".format(album_id))
    album = cursor.fetchone()

    album_name, release_time = album["album_name"], album["release_time"]

    cursor = g.conn.execute("SELECT S.song_id, S.name, S.rel_time FROM song S WHERE S.album_id={}".format(album_id))
    songs = []
    for res in cursor:
        songs.append( {
            "song_id": res["song_id"],
            "name": res["name"],
            "rel_time": res["rel_time"]
        })

    artist_name = ""
    artist_id = ""
    cursor_artist = g.conn.execute("SELECT A.artist_id, A.artist_name FROM artist A INNER JOIN artist_of P ON A.artist_id = P.artist_id WHERE P.album_id={}".format(album_id))
    for res in cursor_artist:
      artist_id = res["artist_id"]
      artist_name = res["artist_name"]

    cursor_record = g.conn.execute("SELECT R.name FROM record R INNER JOIN owned_by O on R.record_id = O.record_id WHERE O.album_id={}".format(album_id))
    for res in cursor_record:
      record_name = res["name"]

    context = {
        "album_id": album_id,
        "record": record_name,
        "name": album_name,
        "release_time": release_time,
        "song_list": songs,
        "artist_name": artist_name,
        "aid": artist_id
    }

    return render_template("album.html", **context)

@app.route('/artist/<aid>')
def artist(aid):
    cursor = g.conn.execute("SELECT * FROM artist WHERE artist_id={}".format(aid))
    artist = cursor.fetchone()

    artist_name, aid, age= artist["artist_name"], artist["artist_id"], artist["age"]
    cursor = g.conn.execute("SELECT R.album_name, R.album_id, R.release_time FROM album R INNER JOIN artist_of P ON R.album_id=P.album_id WHERE P.artist_id={}".format(aid))
    albums = []
    for res in cursor:
        albums.append( {
            "name": res["album_name"],
            "album_id": res["album_id"],
            "release_time": res["release_time"]
        })

    follows = False
    if request.cookies.get('uid'):
        logged_in_uid = request.cookies.get('uid')

        cursor = g.conn.execute("SELECT * FROM followed_by WHERE artist_id={} and user_id={}".format(aid, logged_in_uid))
        if cursor.fetchone() is not None:
            follows = True

    context = {
        "aid": aid,
        "name": artist_name,
        "age": age,
        "album_list": albums,
        "follows": follows
    }

    return render_template("artist.html", **context)


@app.route('/genre')
def genre():
    cursor = g.conn.execute("SELECT * FROM genre")
    genres = []
    for res in cursor:
      genres.append({
        "name": res["name"],
        "id": res["genre_id"],
      })
    context = {
        "genre_list": genres
    }
    return render_template("genre.html", **context)





@app.route('/create_playlist', methods=["GET", "POST"])
def create_playlist():
    if request.method == "GET":
        context = {"error_msg": ""}
        return render_template('create_playlist.html', **context)
    else:
        context = {"error_msg": ""}
        p_name = request.form["name"]
        if len(p_name) > 50:
            context["error_msg"] = "Name must be 50 characters or less"
            return render_template('create_playlist.html', **context)
        if p_name == "":
            context["error_msg"] = "Name can't be empty"
            return render_template('create_playlist.html', **context)
        uid = request.cookies.get('uid')
        pid = str(uid) + str(randint(10, 999))
        is_public = request.form.get('is_public')
        if is_public is None:
            context = {"error_msg": "You must choose private/public"}
            return render_template('create_playlist.html', **context)

        # g.conn.execute("INSERT INTO playlist_createdby (playlist_id, name, creator_user_id, is_public) VALUES({}, '{}', {}, '{}')".format(pid, p_name, uid, is_public))
        g.conn.execute("INSERT INTO playlist_createdby (playlist_id, name, time, creator_user_id, is_public) VALUES({}, '{}','{}','{}', '{}')".format(pid, p_name, datetime.date.today(), uid, is_public))
        return redirect("/playlist/" + str(pid))


@app.route('/playlist/<pid>', methods=["GET", "POST"])
def playlist(pid=None):
    cursor = g.conn.execute("SELECT * FROM playlist_createdby WHERE playlist_id={}".format(pid))
    playlist = cursor.fetchone()
    name, playlist_id, time, no_of_songs, creator_user_id, is_public = playlist["name"], playlist["playlist_id"], playlist["time"], playlist["no_of_songs"], playlist["creator_user_id"], playlist["is_public"]
    cursor = g.conn.execute("SELECT users.name FROM users WHERE users.user_id={}".format(creator_user_id))
    creator_name = cursor.fetchone()["name"]

    subscribes = False
    if request.cookies.get('uid'):
        logged_in_uid = request.cookies.get('uid')
        if int(logged_in_uid) == int(creator_user_id):
            subscribes = True
        cursor = g.conn.execute("SELECT playlist_id, user_id FROM starred_by WHERE playlist_id={} AND user_id={}".format(pid, logged_in_uid))
        if cursor.fetchone() is not None:
            subscribes = True
    
    if is_public == False and int(logged_in_uid) != int(creator_user_id):
        context = {"error_msg": "Sorry, the page you requested to visit is private"}
        return render_template("wrongpage.html", **context)
    cursor = g.conn.execute("SELECT S.name, S.song_id FROM song S INNER JOIN is_in P ON S.song_id=P.song_id WHERE P.playlist_id={}".format(pid))
    songs = []
    for res in cursor:
        songs.append( {
            "name": res["name"],
            "song_id": res["song_id"]
        })

    # cursor_user = g.conn.execute("SELECT U.name FROM users U WHERE U.user_id={}")
    # for res in cursor_user:
    #   username = res["name"]

    context = {
        "playlist_id": playlist_id,
        "name": name,
        "creator_name": creator_name,
        "time": time,
        "no_of_songs": no_of_songs,
        "creator_user_id": creator_user_id,
        "is_public": is_public,
        # "username": username,
        "song_list": songs,
        "stars": subscribes
    }

    return render_template("playlist.html", **context)


@app.route('/user/', methods=["GET"])
def user_default():
    if not request.cookies.get('uid'):
        return redirect("/login")
    else:
        uid = request.cookies.get('uid')
        return redirect("/user/" + uid)


@app.route('/user/<uid>', methods=["GET", "POST"])
def user(uid=None):
    cursor = g.conn.execute("SELECT * FROM users WHERE user_id={}".format(uid))
    user = cursor.fetchone()
    username = user["name"]

    is_user = False
    if request.cookies.get('uid') and request.cookies.get('uid') == uid:
        is_user = True

    # follows = False
    # if request.cookies.get('uid'):
    #     logged_in_uid = request.cookies.get('uid')
    #     if logged_in_uid == uid:
    #         follows = True

    #     cursor = g.conn.execute("SELECT user_id, artist_id FROM followed_by WHERE user_id={}",uid)
    #     if cursor.fetchone() is not None:
    #         follows = True

    cursor = g.conn.execute("SELECT A.artist_id, A.artist_name FROM artist A INNER JOIN followed_by F on A.artist_id = F.artist_id WHERE F.user_id={}".format(uid))
    following = []
    for res in cursor:
        following.append( {
            "artist_name": res["artist_name"],
            "artist_id": res["artist_id"]
        })

    cursor_created_playlists = g.conn.execute("SELECT P.playlist_id, P.name FROM playlist_createdby P WHERE P.creator_user_id={}".format(uid))
    created_playlists = []
    for res in cursor_created_playlists:
      created_playlists.append({
        "playlist_id": res["playlist_id"],
        "name": res["name"]
      })
    
    cursor_subscribed_playlists = g.conn.execute("SELECT P.playlist_id, P.name FROM playlist_createdby P INNER JOIN starred_by S ON P.playlist_id=S.playlist_id WHERE S.user_id={}".format(uid))
    subscribed_playlists = []
    for res in cursor_subscribed_playlists:
      subscribed_playlists.append({
        "playlist_id": res["playlist_id"],
        "name": res["name"]
      })

    context = {
        "uid": uid,
        "username": username,
        "following_artists": following,
        "created_playlists": created_playlists,
        "starring_playlists": subscribed_playlists,
        # "follows": follows,
        "is_user": is_user
    }

    return render_template("user.html", **context)


@app.route('/logout')
def logout():
    uid = request.cookies.get('uid')
    res = flask.make_response(redirect('/login/'))
    res.set_cookie('uid', uid, max_age=0)

    return res


@app.route('/login/', methods=["GET", "POST"])
def login():
    context = {"error_msg": ""}
    if request.method == "POST":
        username = request.form['username'].strip()
        d = {"username": username}
        userinfo = g.conn.execute(text("""SELECT user_id, password FROM users WHERE name=:username"""), **d).fetchone()
        # If incorrect username is entered
        if userinfo is None:
            context["error_msg"] = "Username not found."
            return render_template("login.html", **context)
        user = userinfo["user_id"]
        password = userinfo["password"]
        
        if str(request.form['password']) == str(password):
            uid = user
            res = flask.make_response(redirect('/user/' + str(uid)))
            res.set_cookie('uid', str(uid))
            return res
        else:
            context["error_msg"] = "Wrong password."
            return render_template("login.html", **context)

    else:
        return render_template("login.html", **context)


@app.route('/create/', methods=["GET", "POST"])
def create():
    context = {"error_msg": ""}
    if request.method == "POST":
        username = request.form["username"].strip()
        d = {"username": username}
        if d["username"] == "":
            context["error_msg"] = "Your name can't be empty"
            return render_template("create.html", **context)

        cursor = g.conn.execute("SELECT user_id FROM users WHERE name='{}'".format(username))
        if cursor.fetchone() is not None:
            context["error_msg"] = "Name already exists"
            return render_template("create.html", **context)

        d["uid"] = randint(1000, 99999)
        d["dob"] = request.form["dob"]
        if d["dob"] == "":
            context["error_msg"] = "Date of birth can't be empty"
            return render_template("create.html", **context)
        d["log_in"] = request.form["log_in"]
        if d["log_in"] == "":
            context["error_msg"] = "Username can't be empty"
            return render_template("create.html", **context)
        d["password"] = request.form["password"]
        if d["password"] == "":
            context["error_msg"] = "Password can't be empty"
            return render_template("create.html", **context)
        g.conn.execute(text("""INSERT INTO users(name, user_id, dob, log_in, password) VALUES (:username, :uid, :dob, :log_in, :password)"""), **d)
        uid = g.conn.execute(text("""SELECT user_id FROM users WHERE name=:username"""), **d).fetchone()["user_id"]
        res = flask.make_response(redirect('/user/' + str(uid)))
        res.set_cookie('uid', str(uid))
        return res
    else:
        return render_template("create.html", **context)


@app.route('/follow/', methods=["POST"])
def follow():
    if not request.cookies.get('uid'):
        return redirect('/login/')

    curr_uid = request.cookies.get('uid')
    to_follow = request.form["artist_id"]
    g.conn.execute("INSERT INTO followed_by(artist_id, user_id) VALUES({}, {})".format(to_follow, curr_uid))
    return redirect('/artist/' + to_follow)

@app.route('/add_to_playlist', methods=["POST"])
def add_to_playlist():
    if not request.cookies.get('uid'):
        return redirect('/login/')
        
    song_id = request.form["song_id"]
    playlist_name = request.form["playlist_name"]
    if playlist_name == "":
        context = {"error_msg": "Playlist name can't be empty"}
        return render_template("wrongpage.html", **context)
    cursor = g.conn.execute("select playlist_id, creator_user_id from playlist_createdby where name = '{}'".format(playlist_name))
    pids = cursor.fetchone()
    if pids is None:
        context = {"error_msg": "Playlist does not exist."}
        return render_template("wrongpage.html", **context)
    pid = pids["playlist_id"]
    creator_user_id = pids["creator_user_id"]
    curr_uid = request.cookies.get('uid')
    if str(curr_uid) != str(creator_user_id):
        context = {"error_msg": "You can only add to playlists created by you"}
        return render_template("wrongpage.html", **context)
    
    cursor = g.conn.execute("select * from is_in where playlist_id = {} and song_id = {}".format(pid, song_id))
    res = cursor.fetchone()
    if res is not None:
        context = {"error_msg": "Song already exists in the playlist"}
        return render_template("wrongpage.html", **context)
    g.conn.execute("INSERT INTO is_in (song_id, playlist_id) VALUES({}, {})".format(song_id, pid))
    return redirect("/playlist/" + str(pid))

# @app.route('/insert')
# def insert():
#     genre_names = ['Rock', 'Hip-Hop', 'Jazz', 'Blues', 'Indie']

#     genre_urls = ["https://www.last.fm/tag/rock/albums",
#                   "https://www.last.fm/tag/hip-hop/albums",
#                   "https://www.last.fm/tag/jazz",
#                   "https://www.last.fm/tag/blues",
#                   "https://www.last.fm/tag/indie"]
 
#     # Insert record labels
#     records_labels = [{"label_name":'VirginRecords', "lid":14},{"label_name":'Island Records', "lid":15},{"label_name":'Warner Music Group', "lid": 16},{"label_name":'Red Hill Records', "lid":17},
#                         {"label_name":'Universal Music Publishing Group', "lid":18},{"label_name":'Sony Music Entertainment', "lid":19}]
#     for i in records_labels:
#         g.conn.execute("""INSERT INTO record(record_id, name) VALUES ({},'{}') ON CONFLICT DO NOTHING""".format(i["lid"], i["label_name"]))


#     artists = {}
#     artist_count = 0
#     for i, url in enumerate(genre_urls):
#         data = get_genre_data(url)
#         albums = []
#         labels = []
#         # print(len(data))

#         # Insert genre
#         g.conn.execute("""INSERT INTO genre (genre_id, name) VALUES({}, '{}')
#                                         ON CONFLICT DO NOTHING""".format(str(i + 1), genre_names[i]))

        
#         for d in data:
#             # Get album data
#             album_name = d["album_name"]
#             album_url = d["album_url"]
#             artist_name = d["artist_name"]
#             artist_url = d["artist_url"]
#             album_id = d["album_id"]


#             album_data = get_album_data(d["album_url"])
#             album_date = album_data["release_date"]

#             # Record Label
#             record = get_label_data()
#             record_id = record["lid"]
#             record_name = record["label_name"]
            
#             # Insert album
#             g.conn.execute("""INSERT INTO album (album_id, album_name, release_time) VALUES({}, '{}', '{}')
#                                 ON CONFLICT DO NOTHING;""".format(album_id, album_name.replace("'",""), album_date))

#             # Insert artist
#             if (artist_name not in artists):
#                 g.conn.execute("""INSERT INTO artist (artist_id, artist_name, age) VALUES({}, '{}', {})
#                                     ON CONFLICT DO NOTHING;""".format(artist_count, artist_name.replace("'",""), np.random.randint(25,40)))
#                 artists[artist_name] = artist_count
#                 artist_count += 1

#             # Insert artist_of_album
#             g.conn.execute("""INSERT INTO artist_of (artist_id, album_id) VALUES({}, {})
#                                 ON CONFLICT DO NOTHING;""".format(artists[artist_name], album_id))

#             # Insert album owned_by record
#             g.conn.execute("""INSERT INTO owned_by (record_id, album_id) VALUES({},{})
#                                 ON CONFLICT DO NOTHING;""".format(record_id, album_id))

#             for song in album_data["song_list"]:
#                 song_id = song["sid"]
#                 song_name = song["song_name"]
#                 # Insert song
#                 g.conn.execute("""INSERT INTO song (song_id, name, rel_time, album_id) VALUES({}, '{}', '{}', {})
#                                 ON CONFLICT DO NOTHING;""".format(song_id, song_name[:20].replace("'",""), album_date, album_id))
#                 g.conn.execute("""INSERT INTO belongs_to (song_id, genre_id) VALUES({},{}) ON CONFLICT DO NOTHING;""".format(song_id, str(i+1)))



#     return "Success"

@app.route('/unfollow/', methods=["POST"])
def unfollow():
    if not request.cookies.get('uid'):
        return redirect('/login/')

    curr_uid = request.cookies.get('uid')
    to_follow = request.form["artist_id"]
    g.conn.execute("DELETE FROM followed_by WHERE user_id={} and artist_id={}".format(curr_uid, to_follow))
    return redirect('/artist/' + to_follow)

@app.route('/star/', methods=["POST"])
def star():
    if not request.cookies.get('uid'):
        return redirect('/login/')

    curr_uid = request.cookies.get('uid')
    to_follow = request.form["playlist_id"]
    g.conn.execute("INSERT INTO starred_by(playlist_id, user_id) VALUES({}, {})".format(to_follow, curr_uid))
    return redirect('/playlist/' + to_follow)

@app.route('/unstar/', methods=["POST"])
def unstar():
    if not request.cookies.get('uid'):
        return redirect('/login/')

    curr_uid = request.cookies.get('uid')
    creator_user_id = request.form["creator_user_id"]
    if str(curr_uid)==str(creator_user_id):
        context = {"error_msg": "You can't unsubscribe playlists created by yourself"}
        return render_template("wrongpage.html", **context)
    to_follow = request.form["playlist_id"]
    g.conn.execute("delete from starred_by where user_id={} and playlist_id={}".format(curr_uid, to_follow))
    return redirect('/playlist/' + to_follow)

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
      """
      This function handles command line parameters.
      Run the server using:

          python server.py

      Show the help text using:

          python server.py --help

      """
      HOST, PORT = host, port
      print("running on %s:%d" % (HOST, PORT))
      app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
