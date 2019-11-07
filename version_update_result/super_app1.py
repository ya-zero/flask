import flask
import time
import rq
from redis import Redis
import redis_connect
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

app = flask.Flask(__name__)

@app.route('/send_command')
def index():
    result=redis_connect.redis_send('192.168.0.141','sh ver')
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('result.html')
    return flask.Response(tmpl.generate(result=result.id))

@app.route('/result/<string:id>')
def result(id):
    queue= rq.Queue('microblog',connection=Redis.from_url('redis://'))
    task_que=queue.fetch_job(id)
    print (task_que.result)
    return flask.render_template('result.html',result=task_que.result)
app.run(debug=True)