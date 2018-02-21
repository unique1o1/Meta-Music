from flask import Flask, request, render_template, jsonify
import multiprocessing
from multiprocessing import Pool
import time
import os
import numpy as np

from model import db, fetcher_database
import random
from fetcher import process_init
app = Flask(__name__, static_folder="./static/dist",
            template_folder="./static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@localhost:5432/metamusic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "thisisyunik"
db.init_app(app)


@app.route('/')
def index():

    return render_template('index.html')


@app.route("/process", methods=["GET"])
def process():

    path = request.args['path']
    total_songs = 0
    p = Pool()
    for root, dirs, files in os.walk(path):

        results = p.map(f, files)
        total_songs += np.sum(np.array(results) > 0)
    p.close()
    p.join()
    t = multiprocessing.Process(target=process_init, args=(path, app, db))
    # t.daemon = True
    t.start()
    time.sleep(2)
    return render_template("process.html", totalsongs=total_songs)


@app.route('/fetch/<int:no>')
def fetch(no):
    return_data = fetcher_database.query.filter_by(uid=no).first()

    if return_data is None:
        return 0

    return jsonify(trackname=return_data.trackname, tracknumber=return_data.tracknumber, albumname=return_data.albumname, image_url=return_data.image_url, releasedate=return_data.releasedate,
                   genre=return_data.genre, artistname=return_data.artistname, uid=return_data.uid, loading=True)


def f(n):
    if (n.endswith('.mp3')):
        return 1
    else:
        return 0


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
