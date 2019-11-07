import yaml
import subprocess
import threading
import netmiko

from flask import Flask, render_template, url_for,flash,redirect
from flask_bootstrap import Bootstrap
from super_app_forms import SendCommandForm,DeviceCommandForm,PingForm

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

@myapp.route('/devices', methods=['GET', 'POST'])
def devices():
    form = DeviceCommandForm()
    if form.validate_on_submit():
     with open ('devices.yaml') as f:
            devices = yaml.load(f)
     for i in devices:
         if i['Ip'] == form.ipaddress.data:
            dev=i
            return  render_template('devices.html',dev=dev,form=form)
    return  render_template('devices.html',form=form)

@myapp.route('/all_devices', methods=['GET', 'POST'])
def all_devices():
    with open ('devices.yaml') as f:
            devices = yaml.load(f)
    return  render_template('devices_all.html',devices=devices)


# передача переменных
@myapp.route('/ping' , methods=['GET', 'POST'])
def ping_host():
    form = PingForm()
    if form.validate_on_submit():
        if subprocess.run(['ping',form.ipaddress.data,'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
           result = 'is ok'
           flash ("ping ok")
#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
        else:
           result = "no ping"
           flash ("no ping")
#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
    return render_template('ping.html',form=form)


# передача переменных
@myapp.route('/send_command' , methods=['GET', 'POST'])
def send_command():
    form = SendCommandForm()
    if form.validate_on_submit():
        if subprocess.run(['ping',form.ipaddress.data,'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
           result = 'is ok'
           try:
            device={'device_type':'cisco_ios_telnet','username':'admin','password':'reinfokom','ip':form.ipaddress.data}
            print (device,'\n',form.command.data)
            with netmiko.ConnectHandler(**device,verbose=True) as ssh:
              print ('>>>try connect to host',device['ip'])
              result_command=ssh.send_command(form.command.data)
              if 'Incomplete' in result:
                  print ('Error in command')
              print ('result_connection_to_dev',result_command)
              flash ('')
              return render_template('send_command.html',result_command=result_command,form=form)
           except:
              print ('>>>netmiko_return_error',device['ip'])


#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
        else:
           result = "no ping"
           flash ("no ping")
#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
    return render_template('send_command.html',form=form)



if __name__ == "__main__":
   myapp.run(debug=True, port = 5000)
