import yaml
import subprocess

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from super_app_forms import SendCommandForm
#экземляр myapp класса Flask
#name будет равен имени скрипта или пакета, либо main в нашем варианте
myapp = Flask(__name__)


boostrap=Bootstrap(myapp)
myapp.config['SECRET_KEY']= 'superkey'
myapp.config['WTF_CSRF_ENABLE']= 'False'
#декоратор соотвествие ссылки и функции
#создание маршрутов


@myapp.route('/')
def page():
    return  render_template('index.html') 

@myapp.route('/devices')
def devices():
    with open ('devices.yaml') as f:
          devices = yaml.load(f)
    return  render_template('devices.html',device=devices)


# передача переменных
@myapp.route('/ping/<host>' , methods=['GET', 'POST'])
def ping_host(host):
    form = SendCommandForm()
    if form.validate_on_submit():
  #    print('try ping to host:',host)
       if subprocess.run(['ping',host,'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
           result = 'is ok'
#          return ('is ok')
           return  render_template('send_command.html',host=host,result=result,form=form)
       else:
           result = "no ping"
           return "no ping"
#   render_tamplate('send_command.html',ip=host,result=result)


if __name__ == "__main__":
   myapp.run(debug=True, port = 5000)
