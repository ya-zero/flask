import flask
import time

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

app = flask.Flask(__name__)

@app.route('/send_command')
def index():
    def inner():
        for x in range(100):
            time.sleep(1)
            yield '%s<br/>\n' % x

    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('result.html')
    return flask.Response(tmpl.generate(result=inner()))

app.run(debug=True)