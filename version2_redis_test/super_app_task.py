# -*- coding: utf-8 -*-
import redis_ssh
import time
import yaml
import subprocess
import threading
import netmiko
import mysql
from flask import Flask, render_template, url_for,flash,redirect,jsonify,request
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


# передача переменных
@myapp.route('/redis_send_command' , methods=['GET', 'POST'])
def redis_send_command():
    form = SendCommandForm()
    if form.validate_on_submit():
        job=redis_ssh.redis_send(form.ipaddress.data,form.command.data)
        response_object = {
        'status': 'success',
        'data': {
            'task_id': job.get_id() }
        }
        return jsonify(response_object), 202
#        return render_template('redis_result.html',form=form,job=job)
    return render_template('redis_send_command.html',form=form)


@myapp.route('/tasks', methods=['GET','POST'])
def run_task():
    task_type = request.form['type']
    return jsonify(task_type), 202



if __name__ == "__main__":
   myapp.run(debug=True, port = 5000)
