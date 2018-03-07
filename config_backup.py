#! /usr/bin/env python

""" 
     This script makes backups of statrup configs for several types of network devices

     Usage: py -i device_ip -l tftp_ip  -p paswd  -u username -t cisco-ios
     
     Author: Dmytro Zaskochenko
"""


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
parser.add_argument('-v','--vrf', help='vrf name', required=False)
parser.add_argument('-t','--systype', help='type of the router OS: cisco-ios, cisco-nxos, fortigate, vyos', required=True)
args = vars(parser.parse_args())

ip = args['ipaddress']
uname = args['username']
tftp_location = args['location']
passwd = args['password']
system_type = args ['systype']
vrf_name = args ['vrf']


def CreateQuerySting (tftp_ip, rtr_name, sys_type):
    time_stamp = time.strftime("%Y%m%d-%H%M%S")
    if sys_type == "cisco-ios":
        query_string = "copy startup-config tftp://%s/%s-%s-confg\n\n\n" % (str(tftp_ip), time_stamp, str(rtr_name))
    elif sys_type == "cisco-nxos":
        query_string = "copy startup-config tftp://%s/%s-%s-confg vrf %s\n" % (str(tftp_ip), time_stamp, str(rtr_name), str(vrf_name))
    elif sys_type == "fortigate":
        query_string = "execute backup config tftp  %s-%s-confg %s\n" % (time_stamp, str(rtr_name), str(tftp_ip))
    elif sys_type == "vyos":
        query_string = "copy file running://config/config.boot to tftp://%s/%s-%s-confg\n" % (str(tftp_ip), time_stamp, str(rtr_name))
    return query_string


    

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, port=22, username=uname,  
                        password=passwd,
                        look_for_keys=False, allow_agent=False)

remote_conn = remote_conn_pre.invoke_shell()

time.sleep(.5)
remote_conn.send(CreateQuerySting(tftp_location, ip, system_type))    
time.sleep(.9)
output = remote_conn.recv(100000)
print output

remote_conn_pre.close()
