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
        return 1 if p.poll()==0 else 0
    else:
        return 0

interfaces = netifaces.interfaces()

print ("Las interfaces son: ", interfaces)
dirrecciones_activas = []

for interface in interfaces:
#Se captura la informacion de cada interfaz
    datos = netifaces.ifaddresses(interface)
print ("————————–")
#Se muestra el nombre de la interface
print ("Interface: %s", interface)
#Se captura la lista de parametros que tiene la interface
variables = datos.keys()
#Se muestra la direccion de la capa de enlace de red de la interface
print ("Capa de enlace de red: ", datos[netifaces.AF_LINK][0]['addr'])
#Si esta presente la informacion de IPV4 se muestra
if netifaces.AF_INET in variables:
    print ("IPv4  IP: ",datos[netifaces.AF_INET][0]['addr'],"Mascara:", datos[netifaces.AF_INET][0]['netmask'])
    if(ip_activa(datos[netifaces.AF_INET][0]['addr'])):
        print("IP Activa")
        dirrecciones_activas += datos[netifaces.AF_INET][0]['addr']
    else:
        print("IP no Activa")
#Si esta presente la informacion de IPv6 se muestra
if netifaces.AF_INET in variables:
    print ("IPv6: IP: ",datos[netifaces.AF_INET6][0]['addr'],"Mascara:", datos[netifaces.AF_INET6][0]['netmask'])
    if(ip_activa(datos[netifaces.AF_INET6][0]['addr'])):
        print("Ip Activa")
        dirrecciones_activas += datos[netifaces.AF_INET6][0]['addr']
    else:
        print("IP no Activa")
    



