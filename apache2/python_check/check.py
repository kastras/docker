#!/usr/bin/python3
from urllib.request import ssl, socket
import datetime, smtplib
import os 
import time
port = '443'
context = ssl.create_default_context()
renovar = False
reiniciar = False

def certCheck(hostname):
    try: 
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname = hostname) as ssock:    
                certificate = ssock.getpeercert()
                certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')

                daysToExpiration = (certExpires - datetime.datetime.now()).days

                if daysToExpiration < 3 :
                    return True
    except:
        return True

def getDomains():
    comando = "httpd -S | grep 443 | grep namevhost | awk '{print $4}'"
    return os.popen(comando).read()

def renovarDominio(dominio):
    comando = f"certbot certonly --non-interactive --agree-tos --register-unsafely-without-email -w /var/www/vhosts/{dominio} -d {dominio} --webroot"
    return os.popen(comando).read()

time.sleep(30)

dominios = getDomains()
dominiosArray = dominios.split("\n")
for dominio in dominiosArray:
    renovar = False
    renovar = certCheck(dominio)
    if renovar and dominio != "":
        renovarDominio(dominio)
        reiniciar = True
    else:
        time.sleep(5)

if reiniciar:
    os.kill(1,9)