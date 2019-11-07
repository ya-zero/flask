# -*- coding: utf-8 -*-
# опросить устройства в 192.168.0.0/24
# опросить устройство и сохранить информацию о оборудовании
#"Device Type","Mac","IP Address","Vlan","Boot ver","firmware ver"
#"SNR-S2965-24T","f8:f0:82:75:07:7c","7.0.3.5(R0241.0124)","7.2.25","192.168.0.195"
# заполнить таблицу device.db  sqlite  --> mysql
# сделать многозадачность 
import logging
import telnetlib
import ipaddress
import subprocess
import yaml
import sys
import clitable
import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

# чтение файла устройств
def open_yaml(files_yml):
    with open(files_yml) as f:
        result=yaml.load(f)
    return result

#проверка доступности хоста
def check_device (host):
      result=subprocess.run(['ping',str(host),'-c','1','-W','1'],stdout=subprocess.DEVNULL).returncode
      # если returncode == 0  значит узел доступен.
      return result
#подключение к устройству
def connection_to_dev(device,command):
    try:
      with netmiko.ConnectHandler(**device,verbose=True) as ssh:
          print ('>>>try connect to host',device['ip'])
          #print ('prompt:',ssh.find_prompt())
          ssh.send_command('disable clipaging')
          result=ssh.send_command(command)
          ssh.send_command('enable clipaging')
          if 'Incomplete' in result:
              print ('Error in command')
      return result
    except:
      print ('>>>netmiko_return_error',device['ip'])



try:
  vendor=sys.argv[1]
  ipaddr=sys.argv[2]
  command='''enable lldp\n\r
config lldp ports 9-10 admin_status tx_and_rx\n\r
config lldp ports 9-10 basic_tlvs port_description system_name system_description  enable\n\r
save\n\r
y\r'''
             
  print ('Vendor:',vendor,'\nipaddr',ipaddress.ip_network(ipaddr),'\nCommand:',command)
except:
 print('''неверные аргументы
- первый аргумент Vendor : cisco_like
- второй аргумент  диапазон адресов, если нужен один адрес , то указываем /32 маску
- третий аргумент 'show version' / 'show switch'
''')


subnet=ipaddress.ip_network(ipaddr)#подсеть для изучения
#default_param={'device_type':'cisco_ios_telnet','username':'mgmt','password':'1valera2'}#параметры для подключения к оборудованию
default_param={'device_type':'cisco_ios_telnet','username':'mgmt','password':'valera22'}#параметры для подключения к оборудованию


for host in subnet:
    if check_device(host)==0:
      default_param.update({'ip':str(host)})
      result_command=connection_to_dev(default_param,command)
      print (result_command)
    else: print ('no icmp to host',host)

#with open('device_sw.yml','w') as f:
# yaml.dump({'Dlink switch':devices_list},f,default_flow_style=False)

