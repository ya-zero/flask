# -*- coding: utf-8 -*-
from pprint import pprint
import yaml
import subprocess
import threading
import netmiko
import mysql
from redis import Redis
import rq
import redis_connect
from flask import Flask, render_template, url_for,flash,redirect,Response
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
#    a = {'user':{'username':'valera'}}
#    flash('hellppooooo')
    flash("")
    return  render_template('index.html')


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
    startat=(page-1)*perpage
    cursor=mysql.sql_connect()
    sql='''SELECT switches.id,`boot`,`hardware`,`mac`,`serial_number`,vendor.vendor,model.name,model.all_ports,INET_NTOA(ip_address.ip),`software_version`  FROM `switches`
              INNER JOIN `vendor` ON switches.id_vendor=vendor.id INNER JOIN `ip_address` ON switches.id_ip=ip_address.id
              INNER JOIN `model` ON switches.id_model=model.id limit %s,%s'''%(startat,perpage)
    cursor[0].execute(sql)
    result=cursor[0].fetchall()
    sql='''SELECT COUNT(*) FROM `switches`'''
    cursor[0].execute(sql)
    all_rows=cursor[0].fetchone()
    pages=round(all_rows['COUNT(*)']/perpage+0.5)
    return  render_template('devices_all.html',devices=result,pages=pages)


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
           result=redis_connect.redis_send(form.ipaddress.data,form.command.data)
           return redirect ('/result_job/{}'.format(result.id))
    return render_template('send_command.html',form=form)


# передача переменных
@myapp.route('/result_job/<string:id>' , methods=['GET', 'POST'])
def result_job(id):
    queue= rq.Queue('microblog',connection=Redis.from_url('redis://'))
    task_que=queue.fetch_job(id)
    if  task_que:
         return render_template('result_job.html',result=task_que.result )
    return render_template('index.html')



@myapp.route('/update_string/<int:dev>' , methods=['GET', 'POST'])
def update_string(dev):
    form = DeviceEditForm()
    form.test.choices=[]
    sql='SELECT id,INET_NTOA(ip) FROM ip_address WHERE ip_address.id NOT IN (SELECT id_ip FROM switches)'
    result_ip=mysql.select_from_mysql(sql)
    for ip_addr  in result_ip:
         form.test.choices.append((ip_addr['id'],ip_addr['INET_NTOA(ip)']))
    sql='''SELECT switches.id,`boot`,`hardware`,`mac`,`serial_number`,vendor.vendor,model.name,model.all_ports,INET_NTOA(ip_address.ip),`software_version`  FROM `switches`
              INNER JOIN `vendor` ON switches.id_vendor=vendor.id INNER JOIN `ip_address` ON switches.id_ip=ip_address.id
              INNER JOIN `model` ON switches.id_model=model.id WHERE switches.id = "%s" '''%dev
    result=mysql.select_from_mysql(sql)
    return  render_template('devices_edit.html',device=result[0],form=form)



if __name__ == "__main__":
   myapp.run(debug=True, port = 5000)
