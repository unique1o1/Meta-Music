from flask import Flask, request, render_template
import multiprocessing
import time
import random
app = Flask(__name__)


@app.route('/')
def index():

    # t = multiprocessing.Process(target=process)
    # t.start()

    return render_template('index.html')


@app.route("/process", methods=["GET"])
def process():
    a = int(random.random() * 10 % 10)

    print("inside this")
    for i in range(5):

        time.sleep(2)
        print("sleep {}".format(a))
    return render_template("process.html")


if __name__ == "__main__":
    app.run(debug=True)
