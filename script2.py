#!/usr/bin/python3
import netifaces
import socket
import os
import subprocess
def ip_valida(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
def ip_activa(ip):
    if(ip_valida(ip)== True):
        p = subprocess.Popen(['ping', '-n', '2', '-w', '2', ip])
        p.wait()
        return 1 if p.poll()==0 else 1
    else:
        return 0
def obtenerClaseIP(ip):
	direccionip = ip.split('.')
	primerOcteto = int(direccionip[0])
	if(primerOcteto >= 1 and primerOcteto <=127):
		return 'A'
	elif(primerOcteto >=128 and primerOcteto <=191):
		return 'B'
	elif(primerOcteto >= 192 and primerOcteto <= 223):
		return 'C'
	else:
		return 'Unknown'
def aproximarMascara(claseIP):
	if (claseIP == 'A'):
		return '255.0.0.0'
	elif(claseIP == 'B'):
		return '255.255.0.0'
	elif(claseIP=='C'):
		return '255.255.255.0'
	else:
		return 'Unknown'
ip_func = []
masc_func = []
i=0
for iface in netifaces.interfaces():
    if iface == 'lo' or iface.startswith('vbox'):
        continue
    iface_details = netifaces.ifaddresses(iface)
    if iface_details.__contains__(netifaces.AF_INET):
        print ("Tus red es: ", iface_details[netifaces.AF_INET])
        for ip_interface in iface_details[netifaces.AF_INET]:
            for llave, direccion_ip in ip_interface.items():
                if llave== 'addr' and direccion_ip != '127.0.0.1': 
                    if(ip_activa(direccion_ip)):
                        print("IP activa", direccion_ip)
                        ip_func+= str(direccion_ip)
                        masc_func += aproximarMascara(obtenerClaseIP(direccion_ip))





