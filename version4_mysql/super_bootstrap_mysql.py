# -*- coding: utf-8 -*-
from pprint import pprint
import yaml
import subprocess
import threading
import netmiko
import mysql
from flask import Flask, render_template, url_for,flash,redirect
from flask_bootstrap import Bootstrap
from super_app_forms import SendCommandForm,DeviceCommandForm,PingForm,DeviceEditForm

#экземляр myapp класса Flask
#name будет равен имени скрипта или пакета, либо main в нашем варианте
myapp = Flask(__name__)


boostrap=Bootstrap(myapp)
myapp.config['SECRET_KEY']= 'superkey'
myapp.config['WTF_CSRF_ENABLE']= 'False'
#декоратор соотвествие ссылки и функции
#создание маршрутов

@myapp.route('/index')
@myapp.route('/')
def page():
    flash('hellppooooo')
    return  render_template('index.html')
#    return redirect(url_for('page'))
#    cursor=mysql.sql_connect()
#    sql='select * from switches'
#    sql='SELECT switches.id,`boot`,`hardware`,`mac`,vendor.vendor,model.name,model.all_ports,INET_NTOA(ip_address.ip)  FROM `switches` INNER JOIN `vendor` ON switches.id_vendor=vendor.id INNER JOIN `ip_address` ON switches.id_ip=ip_address.id INNER JOIN `model` ON switches.id_model=model.id'
#    sql='SELECT `id`,`boot`,`hardware`,`mac`,`vendor` FROM `switches` LEFT JOIN `vendor` WHERE USING (`id_vendor`)'
#    cursor[0].execute(sql)
#    result=cursor[0].fetchall()
#    print (result)
#    for i in cursor[0]:
#        print (i)
#    return  render_template('index.html',sql=cursor[0])

@myapp.route('/devices', methods=['GET', 'POST'])
def devices():
    form = DeviceCommandForm()
    if form.validate_on_submit():
       cursor=mysql.sql_connect()
       sql='''SELECT switches.id,`boot`,`hardware`,`mac`,`serial_number`,vendor.vendor,model.name,model.all_ports,INET_NTOA(ip_address.ip),`software_version`  FROM `switches`
              INNER JOIN `vendor` ON switches.id_vendor=vendor.id INNER JOIN `ip_address` ON switches.id_ip=ip_address.id
              INNER JOIN `model` ON switches.id_model=model.id WHERE INET_NTOA(ip_address.ip)  LIKE "%{0}%" OR `mac`  LIKE"%{0}%" OR model.name LIKE "%{0}%" '''.format(form.ipaddress.data)
       cursor[0].execute(sql)
       result=cursor[0].fetchall()
       return  render_template('devices_result.html',device=result,form=form)
    return  render_template('devices_request.html',form=form)


@myapp.route('/all_devices', methods=['GET', 'POST'], defaults={'page':1})
@myapp.route('/all_devices/page/<int:page>', methods=['GET', 'POST'],)
def all_devices(page):
    perpage=20
    with open ('devices.yaml') as f:
            devices = yaml.load(f)
    return  render_template('devices_all.html',devices=devices,page=page,perpage=perpage)


# передача переменных
@myapp.route('/ping' , methods=['GET', 'POST'])
def ping_host():
    form = PingForm()
    if form.validate_on_submit():
        if subprocess.run(['ping',form.ipaddress.data,'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
           result = 'is ok'
           flash ("Ping to {} is  ok".format(form.ipaddress.data))
#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
        else:
           result = "no ping"
           flash ("Ping to {} is  not".format(form.ipaddress.data))
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
#              flash ('')
              return render_template('send_command.html',result_command=result_command,form=form)
           except:
              print ('>>>netmiko_return_error',device['ip'])


#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
        else:
           result = "no ping"
           flash ("no ping")
#           return  render_template('send_command.html',host=form.ipaddress.data,result=result,form=form)
    return render_template('send_command.html',form=form)

@myapp.route('/update_string/<int:dev>' , methods=['GET', 'POST'])
def update_string(dev):
    form = DeviceEditForm()
    form.test.choices=[]
    sql='SELECT id,INET_NTOA(ip) FROM ip_address WHERE ip_address.id NOT IN (SELECT id_ip FROM switches)'
    result_ip=mysql.select_from_mysql(sql)
    for ip_addr  in result_ip:
         form.test.choices.append((ip_addr['id'],ip_addr['INET_NTOA(ip)']))
#   
    sql='''SELECT switches.id,`boot`,`hardware`,`mac`,`serial_number`,vendor.vendor,model.name,model.all_ports,INET_NTOA(ip_address.ip),`software_version`  FROM `switches`
              INNER JOIN `vendor` ON switches.id_vendor=vendor.id INNER JOIN `ip_address` ON switches.id_ip=ip_address.id
              INNER JOIN `model` ON switches.id_model=model.id WHERE switches.id = "%s" '''%dev
    result=mysql.select_from_mysql(sql)
    return  render_template('devices_edit.html',device=result[0],form=form)



if __name__ == "__main__":
   myapp.run(debug=True, port = 5000)
