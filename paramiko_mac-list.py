#! /usr/bin/env python

import paramiko
from getpass import getpass
import time
import argparse
import sys

parser = argparse.ArgumentParser(description='pramiko test')
parser.add_argument('-ip','--ipaddress', help='router ip', required=True)
parser.add_argument('-l','--location', help='tftp server ip', required=True)
parser.add_argument('-p','--password', help='cli pass', required=True)
parser.add_argument('-u','--username', help='cli username', required=True)
parser.add_argument('-t','--systype', help='type of the router OS: cisco, vyos', required=True)
args = vars(parser.parse_args())

ip = args['ipaddress']
uname = args['username']
tftp_location = args['location']
passwd = args['password']
system_type = args ['systype']


def CreateQuerySting (tftp_ip, rtr_name, sys_type):
    time_stamp = time.strftime("%Y%m%d-%H%M%S")
    if sys_type == "cisco":
        query_string = "show ip dhcp binding"
    elif sys_type == "vyos":
        query_string = "copy file running://config/config.boot to tftp://%s/%s-%s-confg\n" % (str(tftp_ip), time_stamp, str(rtr_name))
    return query_string


    

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, port=22, username=uname,  
                        password=passwd,
                        look_for_keys=False, allow_agent=False)

remote_conn = remote_conn_pre.invoke_shell()
# output = remote_conn.recv(65535)
# print output


remote_conn.send(CreateQuerySting(tftp_location, ip, system_type))    
time.sleep(1)
output = remote_conn.recv(165535)
print output

remote_conn_pre.close()
