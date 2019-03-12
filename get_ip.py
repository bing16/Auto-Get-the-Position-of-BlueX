#-*-coding: utf-8-*-
import os
import re

def get_ip_address():
    message = os.popen('ifconfig -a').readlines()
    ipaddr = re.findall(r'[i][n][e][t].\d+\.\d+\.\d+\.\d+',str(message))
    ip = re.findall(r'\d+\.\d+\.\d+\.\d+',str(ipaddr[1]))
    return ip[0]

if __name__ == '__main__':
	ip = get_ip_address()
	print(ip)