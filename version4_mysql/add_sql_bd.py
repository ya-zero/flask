#добавление разной ерунды из файлов yaml 
# модели коммутаторов  dlink  snr только уникалных
# наполение таблицы ip addresov    INET_ATON 
#                                  INET_NTOA
 
import mysql
import yaml
from pprint import pprint

#читаем yaml

with open ('devices.yaml') as f:
          devices_snr = yaml.load(f)

with open ('devices_dlink.yaml') as f:
          devices_dlink = yaml.load(f)

'''
list_snr=[]
for i in devices_snr:
    list_snr.append(i['Model'])
list_snr=set(list_snr)

cursor=mysql.sql_connect()
for i in  list_snr:
    print (i)
    sql="INSERT INTO `model`(`id`, `name`, `all_ports`) VALUES (0,"%s",0)"%i
    cursor[0].execute(sql)
cursor[0].close()
cursor[1].commit()
'''
'''
list_dlink=[]
for i in devices_dlink:
    list_dlink.append(i['Model'])

list_dlink=set(list_dlink)


cursor=mysql.sql_connect()
for i in  list_dlink:
    print (i)
    sql="INSERT INTO `model`(`id`, `name`, `all_ports`) VALUES (0,"%s",0)"%i
    cursor[0].execute(sql)
cursor[0].close()
cursor[1].commit()

'''
#cursor=mysql.sql_connect()
#for i in  range(1,255):
#    i="192.168.0."+str(i)
#    sql='''INSERT INTO `ip_address` (`id`,`id_pool`,`id_state`,`ip`) VALUES (0,0,0,INET_ATON("%s"))'''%i
#    cursor[0].execute(sql)
#cursor[0].close()
#cursor[1].commit()

#select   in ipaddress
cursor=mysql.sql_connect()
sql='''SELECT `id`,`id_pool`,`id_state`,INET_NTOA(`ip`) FROM ip_address '''
cursor[0].execute(sql)


#    sql='select * from switches'
    sql='SELECT `boot`,`hardware`,`vendor` FROM `switches` LEFT JOIN `vendor` USING (`id`)'
    cursor.execute(sql)
    for i in cursor:
        print (i)

