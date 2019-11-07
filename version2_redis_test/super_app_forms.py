from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField
from wtforms.validators  import DataRequired,IPAddress

class SendCommandForm(FlaskForm):
      ipaddress = StringField('Ip address',validators=[DataRequired(),IPAddress()])
      command = StringField('Command',validators=[DataRequired()])
      commit = SubmitField('Send')

class PingForm(FlaskForm):
      ipaddress = StringField('Ip address',validators=[DataRequired(),IPAddress()])
      commit = SubmitField('Send')

class DeviceCommandForm(FlaskForm):
#      ipaddress = StringField('IpAddres Switch',validators=[DataRequired(),IPAddress()])
       ipaddress = StringField('IpAddres Switch',validators=[DataRequired()])
#      command = StringField('Command',validators=[DataRequired()])
       commit = SubmitField('Send request')
