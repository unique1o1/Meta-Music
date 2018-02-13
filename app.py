from flask import Flask, request, render_template
import threading
import time
import random
app = Flask(__name__)


@app.route('/')
def index():

    t = threading.Thread(target=process)
    t.start()
    return render_template('index.html')


def process():
    a = int(random.random() * 10 % 10)

    print("inside this")
    for i in range(10):

        time.sleep(2)
        print("sleep {}".format(a))


if __name__ == "__main__":
    app.run(debug=True)
