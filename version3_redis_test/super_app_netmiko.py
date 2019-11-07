from flask import Flask,render_template
import yaml
import subprocess
import netmiko

#экземляр myapp класса Flask
#name будет равен имени скрипта или пакета, либо main в нашем варианте
myapp = Flask(__name__)

#декоратор соотвествие ссылки и функции
#создание маршрутов
@myapp.route('/')
def page():
#    1+'a'
    return  render_template('index.html') 
#    return "network discovery"

@myapp.route('/devices')
def devices():
    with open ('devices.yaml') as f:
          devices = yaml.load(f)
    return  render_template('devices.html',device=devices)


# передача переменных
@myapp.route('/ping/<host>')
def ping_host(host):
    print('try ping to host:',host)
    if subprocess.run(['ping',host,'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
        result = 'is ok'
#        return ('is ok')
        return  render_template('send_command.html',host=host,result=result)
    else:
        result = "no ping"
        return "no ping"
#   render_tamplate('send_command.html',ip=host,result=result)


if __name__ == "__main__":
   myapp.run(debug=True, port = 5000)
