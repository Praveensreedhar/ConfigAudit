from ipaddress import ip_address
import napalm
from napalm import get_network_driver
import netmiko
import openpyxl
import xlsxwriter
import subprocess, sys
from netmiko import ConnectHandler
from netmiko import exceptions
from paramiko.ssh_exception import SSHException
import os
import re
from getpass import getpass, getuser
os.chdir("C:\\Automation\\Config_audit_Script-final")

workbook = xlsxwriter.Workbook('C:\\Automation\\Config_audit_Script-final\\Mini-2.xlsx')
worksheet = workbook.add_worksheet()

cell_format = workbook.add_format({'bold': True, 'font_color': 'white'})
cell_format.set_font_size(12)
cell_format.set_bg_color('blue')

worksheet.write('A1', 'IP Address', cell_format)
worksheet.write('B1', 'Junos/IOS Version', cell_format)
worksheet.write('C1', 'HostName', cell_format)
worksheet.write('D1', 'Location', cell_format)
worksheet.write('E1', 'NTP Configured', cell_format)
worksheet.write('F1', 'FTP', cell_format)
worksheet.write('G1', 'Telnet', cell_format)
worksheet.write('H1', 'Local DHCP', cell_format)
worksheet.write('I1', 'TACACS-Server Host 10.100.91.192', cell_format)
worksheet.write('J1', 'TACACS-Server Host 10.35.91.192', cell_format)
worksheet.write('K1', 'TACACS-Server Host 10.90.91.192', cell_format)
worksheet.write('L1', 'TACACS-Server Host 10.31.91.192', cell_format)
worksheet.write('M1', 'Local Login(rtradmin)', cell_format)

worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 35)
worksheet.set_column('C:C', 20)
worksheet.set_column('D:D', 10)
worksheet.set_column('E:E', 31)
worksheet.set_column('F:F', 31)
worksheet.set_column('G:G', 31)
worksheet.set_column('H:H', 31)
worksheet.set_column('I:I', 20)
worksheet.set_column('J:J', 5)
worksheet.set_column('K:K', 8)
worksheet.set_column('L:L', 13)
worksheet.set_column('M:M', 15)


#workbook.close()

def get_credentials():
    username = input('Enter username : ')
    #password = None
    #while not password:
    password = getpass('Enter password : ')
    return username, password
    
username, password = get_credentials()
device_type = 'juniper'
devices = open('devices.txt')
row = 0

for IP in devices:
    dev = {
         'device_type' : 'juniper',
         'ip' : IP,
         'username' : username,
         'password' : password
          }

    connection_1 = ConnectHandler(**dev)
    ipaddress = IP
    print(ipaddress)
    host_name = connection_1.find_prompt()
    ch = '@'
    pattern  = ".*" + ch
    Hostname1 = re.sub(pattern, '', host_name )
    Hostname1 = Hostname1[:-1]
    print(Hostname1)
    location = Hostname1[ - 3:]
    
    print(location)
    os_version = connection_1.send_command('show version | match Junos:')
    ntp = connection_1.send_command('show configuration | display set | match ntp | match server')
    if not ntp:
        ntp = "No"
    else:
        ntp = "Yes"
    print(ntp)
    ftp = connection_1.send_command('show configuration | display set | match system | match services | match ftp')
    if not ftp:
        ftp = "No"
    else:
        ftp = "Yes" 
    print(ftp)      
    telnet = connection_1.send_command('show configuration | display set | match system | match services | match telnet')
    if not telnet:
        telnet = "No"
    else:
        telnet = "Yes"
    print(telnet)       
    dhcp =  connection_1.send_command('show configuration | display set | match system | match services | match dhcp | match router')
    if not dhcp:
        dhcp = "No"
    else:
        dhcp = "Yes"
    print(dhcp)       
    tacplus_trv = connection_1.send_command('show configuration | display set | match tacplus-server | match 10.100.91.192')
    if not tacplus_trv:
        tacplus_trv = "No"
    else:
        tacplus_trv = "Yes"
    print(tacplus_trv)        
    tacplus_maa = connection_1.send_command('show configuration | display set | match tacplus-server | match 10.35.91.192')
    if not tacplus_maa:
        tacplus_maa = "No"
    else:
        tacplus_maa = "Yes"
    print(tacplus_maa)            
    tacplus_lax = connection_1.send_command('show configuration | display set | match tacplus-server | match 10.31.91.192')
    if not tacplus_lax:
        tacplus_lax = "No"
    else:
        tacplus_lax = "Yes"
    print(tacplus_lax)        
    tacplus_den = connection_1.send_command('show configuration | display set | match tacplus-server | match 10.90.91.192')
    if not tacplus_den:
        tacplus_den = "No"
    else:
        tacplus_den = "Yes"
    print(tacplus_den) 
    local_login = connection_1.send_command('show configuration | display set | match login | match user')
    if not local_login:
        local_login = "No"
    else:
        local_login = "Yes"
    print(local_login)
    connection_1.disconnect()
     
    data1 = [ipaddress, os_version, Hostname1, location, ntp, ftp, telnet, dhcp, tacplus_trv, tacplus_maa, tacplus_lax, tacplus_den, local_login]
    #worksheet.write(1, 0, data1)
    #workbook = xlsxwriter.Workbook('C:\\Automation\\test\\Audit-Report.xlsx')
    #worksheet = workbook.add_worksheet()
    row = row + 1
    for col_num, data in enumerate(data1):
        
        worksheet.write(row, col_num, data)
        
        
workbook.close()
    
    

