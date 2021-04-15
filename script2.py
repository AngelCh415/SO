#!/usr/bin/python3
#Chávez Morones Angel Uriel  2CV16  ESCOM
import netifaces
import socket
import os
import subprocess
import tarfile
def ip_valida(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
def ip_activa(ip):
    if(ip_valida(ip)== True):
        os.system("ping -c1 "+ip)
        return 1 
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
ip_nofunc = []
masc_nofunc = []
i=0
interfaces = netifaces.interfaces()
print ("Interfaces: ", interfaces)
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
                    else:
                        print("IP no activa", direccion_ip)
                        ip_nofunc+= str(direccion_ip)
                        masc_nofunc += aproximarMascara(obtenerClaseIP(direccion_ip))
file = open("Direcciones.txt", "w")
file.write("Ip: " + str(ip_func ) + os.linesep)
file.write("Mascaras:" + str(masc_func) + os.linesep)
file.write("Ip no activa:" + str(ip_nofunc) + os.linesep)
file.write("Mascaras: " + str(masc_nofunc))
file.close()
#Haciendo el archivo tar

with tarfile.open('Direcciones.tar', mode='w') as out:
    out.add('Direcciones.txt')
print("Enviando el archivo")
from socket import socket
s = socket()
s.connect(("localhost", 8000))
while True:
    f = open("Direcciones.tar", "rb")
    content = f.read(1024)
        
    while content:
        s.send(content)
        content = f.read(1024)        
    break
try:
    s.send(chr(1))
except TypeError:
    s.send(bytes(chr(1), "utf-8"))
s.close()
f.close()
print("El archivo ha sido enviado correctamente.")
