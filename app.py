from flask import Flask, request, render_template
import multiprocessing
import time
from model import db
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
    # a = int(random.random() * 10 % 10)

    # print("inside this")
    # for i in range(5):

    #     time.sleep(2)
    #     print("sleep {}".format(a))
    path = request.args['path']

    t = multiprocessing.Process(target=process_init, args=(path, app,db))
    t.start()

    return render_template("process.html")


if __name__ == "__main__":
    app.run(debug=True)
