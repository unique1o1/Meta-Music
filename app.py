from flask import Flask, request, render_template, jsonify, abort
import multiprocessing
from multiprocessing import Pool
import time
import os
import numpy as np
import webbrowser
import string
import glob
import random
from model import db, fetcher_database
import random
import os
from fetcher import process_init
app = Flask(__name__, static_folder="./static/dist",
            template_folder="./static")

database_name = ''.join(random.choices(
    string.ascii_uppercase, k=10))
db_path = os.getcwd()
for i in glob.glob(os.path.join(db_path, '*.db')):
    os.remove(i)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    db_path + '/' + database_name + '.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "thisisyunik"
db.init_app(app)


@app.route('/')
def index():

    return render_template('index.html')


@app.route("/process", methods=["GET"])
def process():

    path = request.args['path']
    if not os.path.exists(path):
        time.sleep(.3)
        return render_template("nofile.html")
    total_songs = 0

    if not os.path.isfile(path):
        p = Pool()
        folders = []
        for root, dirs, files in os.walk(path):

            results = p.map(f, files)
            numbers = np.sum(np.array(results) > 0)
            if numbers:
                folders.append(root)
            total_songs += numbers
        p.close()
        p.join()

        t = multiprocessing.Process(
            target=process_init, args=(path, app, db, folders))
    else:
        total_songs = 1
        folders = [os.path.dirname(path)]
        t = multiprocessing.Process(
            target=process_init, args=(path, app, db, folders))
    t.daemon = True
    t.start()
    time.sleep(0.4)
    return render_template("process.html", totalsongs=total_songs)


@app.route('/fetch/<int:no>')
def fetch(no):
    return_data = fetcher_database.query.filter_by(uid=no).first()

    while return_data is None:
        time.sleep(0.01)
        return_data = fetcher_database.query.filter_by(uid=no).first()
    if not return_data.status:
        return abort(404)
    return jsonify(trackname=return_data.trackname, tracknumber=return_data.tracknumber, albumname=return_data.albumname, image_url=return_data.image_url, releasedate=return_data.releasedate,
                   genre=return_data.genre, artistname=return_data.artistname, uid=return_data.uid, loading=True)


def f(n):
    if (n.endswith('.mp3')):
        return 1
    else:
        return 0


if __name__ == "__main__":

    app.run(debug=True, threaded=True)
