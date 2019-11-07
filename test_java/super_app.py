import time
from flask import Flask, jsonify
from flask import render_template
from threading import Thread

app = Flask(__name__)
th = Thread()
finished = False


#@app.route("/")
#def init():
#    return render_template('index.html')


@app.route("/", methods=['POST','GET'])
def load():
    global th
    global finished
    finished = False
#    th = Thread(target=something, args=())
#    th.start()
    return render_template('loading.html')


def something():
    """ The worker function """
    global finished
    time.sleep(5)
    finished = True


@app.route('/result')
def result():
    """ Just give back the result of your heavy work """
    return 'Done'


@app.route('/status')
def thread_status():
    """ Return the status of the worker thread """
    return jsonify(dict(status=('finished' if finished else 'running')))


if __name__ == "__main__":
    app.run(debug=True)