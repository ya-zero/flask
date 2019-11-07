import netmiko
import subprocess
import time

def send_command(ipaddr,command):
        if subprocess.run(['ping',ipaddr,'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
           result = 'is ok'
           try:
            device={'device_type':'cisco_ios_telnet','username':'admin','password':'reinfokom','ip':ipaddr}
            print (device,'\n',command)
            with netmiko.ConnectHandler(**device,verbose=True) as ssh:
              print ('>>>try connect to host',device['ip'])
              result_command=ssh.send_command(command)
              if 'Incomplete' in result:
                  print ('Error in command')
              print ('result_connection_to_dev',result_command)
              return result_command
           except:
              print ('>>>netmiko_return_error',device['ip'])
              return ('>>>netmiko_return_error',device['ip'])
if __name__ == "__main__":
   print (send_command('192.168.0.141','sh ver'))
