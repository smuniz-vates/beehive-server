#!/usr/bin/env python
import web
import os.path
import subprocess
import threading


# apt-get install python-webpy
# pip install web.py


resource_lock = threading.RLock()

def read_file( str ):
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""





urls = (
    '/certca', 'certca',
    '/newnode', 'newnode',
    '/(.*)', 'use resources /certca and /newnode'
)

app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'world'
        return 'Hello, ' + name + '!'

class certca:        
    def GET(self):
        result = read_file("/usr/lib/waggle/SSL/waggleca/cacert.pem")
        if not result:
            return "error: cacert file not found !?"

        return result

class newnode:        
    def GET(self):

        privkey=""
        cert=""
        with resource_lock:
            subprocess.call(['/usr/lib/waggle/beehive-server/SSL/create_client_cert.sh', 'node', 'temp_client_cert'])
            privkey = read_file("/usr/lib/waggle/SSL/temp_client_cert/key.pem")
            cert = read_file("/usr/lib/waggle/SSL/temp_client_cert/cert.pem")
            
        if not privkey:
            return "error: privkey file not found !?"
        
        if not cert:
            return "error: cert file not found !?"

        return privkey + "\n" + cert


if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 9999))
    app.run()

# docker run -ti -p 9999:9999 -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/  waggle/beehive-server /bin/bash
# cd /usr/lib/waggle/beehive-server/cert-serve ; ./cert-serve.py


