import mysql
import yaml
import re
from pprint import pprint




with open('devices_dlink.yaml') as f:
     device_dlink=yaml.load(f)

with open('devices.yaml') as f:
     device_snr=yaml.load(f)

all_dev=device_dlink+device_snr

cursor=mysql.sql_connect()
for i in  all_dev:
    print("------------------------------------")
    vendor=''
    print (i)
    #ищем в базе id vendor
    pattern="SNR|DES|DGS"
    reg=re.match(pattern,i['Model'])
    if 'DES' or "DGS" in reg[0]:
        vendor="D-link"
    if 'SNR'  in reg[0]:
        vendor="SNR"
    sql='''SELECT `id` FROM `vendor` WHERE vendor="%s"'''%vendor
    cursor[0].execute(sql)
    data_vendor=cursor[0].fetchone()
    if data_vendor:
        id_vendor=data_vendor[0]
        print(id_vendor)
    #ищем в базе id ip
    print(i['Ip'])
    sql='''SELECT `id` FROM `ip_address` WHERE ip=INET_ATON("%s")'''%i['Ip']
    cursor[0].execute(sql)
    data_ip=cursor[0].fetchone()
    if data_ip:
        id_ip=data_ip[0]
        print (id_ip)
    #ищем в базе id model
    sql='''SELECT `id` FROM `model` WHERE name="%s"'''%i['Model']
    cursor[0].execute(sql)
    data_model=cursor[0].fetchone()
    if data_model:
        id_model=data_model[0]

    #подставляем в insert

#    sql="INSERT INTO `switches`(`id`, `name`, `all_ports`) VALUES (0,"%s",0)"%i
    if  i.get('Serial') == None:
          serial="non serial"
    else:
       serial=i['Serial']

    sql='''
    INSERT INTO `switches`(`id`, `boot`, `hardware`, `id_ip`, `id_model`, `serial_number`, `id_vendor`, `software_version`,`mac`)
    VALUES (0,"%s","%s",%s,%s,"%s",%s,"%s","%s")'''%(i['Boot'],i['Hardware'],id_ip,id_model,serial,id_vendor,i['Software'],i['Mac'])
    cursor[0].execute(sql)

cursor[0].close()
#cursor[1].commit()

