#coding=utf-8
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import subprocess
from os import system, chdir, getcwd
import shutil
from time import time

class RequestHandler(SimpleXMLRPCRequestHandler):
    rc_paths = ('/RPC2',)


vtid = 0
vtask_list = []
basedir = getcwd()

def executa_comando(name):
    global basedir
    chdir(basedir)
    get = subprocess.Popen(name, shell=True, stdout=subprocess.PIPE)
    out = get.communicate()[0]
    chdir('../')
    return out

# Cria uma nova vtask
def vtask_new():
    global vtid
    global basedir
    vtid += 1
    name = str(time())+"vtask"
    vtask_list.append({'vtid':vtid, 'name':name})
    create = subprocess.Popen('virtualenv '+name, shell=True, stdout=subprocess.PIPE)
    out = create.communicate()
    basedir += "/"+name
    return vtid

# Destroy uma vtask
def vtask_kill(vtid):
    global vtask_list
    l = [item for item in vtask_list if item['vtid'] == vtid]
    if len(l) > 0:
        vtask = l[0]
        shutil.rmtree(vtask['name'])
        vtask_list.remove(vtask)


server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()
server.register_function(pow)
server.register_function(vtask_new)
server.register_function(vtask_kill)
server.register_function(executa_comando)
server.register_function(lambda x,y: x+y, 'add')

server.serve_forever()
