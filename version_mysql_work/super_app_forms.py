import mysql
from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField,SelectField
from wtforms.validators  import DataRequired,IPAddress

class SendCommandForm(FlaskForm):
      ipaddress = StringField('Ip address',validators=[DataRequired(),IPAddress()])
      command = StringField('Command',validators=[DataRequired()])
      commit = SubmitField('Send')

class PingForm(FlaskForm):
      ipaddress = StringField('Ip address',validators=[DataRequired(),IPAddress()])
      commit = SubmitField('Send')

class DeviceCommandForm(FlaskForm):
       ipaddress = StringField('Search device ',validators=[DataRequired()])
       commit = SubmitField('Send request')

class DeviceEditForm(FlaskForm):
       boot = StringField('Boot',validators=[DataRequired()])
       hardware = StringField('Hardware',validators=[DataRequired()])
       ip = StringField('Ip',validators=[DataRequired()])
       mac = StringField('Mac',validators=[DataRequired()])
       model = StringField('Model',validators=[DataRequired()])
       serial = StringField('Serial',validators=[DataRequired()])
       software = StringField('Software',validators=[DataRequired()])
       test = SelectField('TEST',choices = [])
       commit = SubmitField('Сохранить')

