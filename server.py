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
DIR = getcwd()
basedir = getcwd()

def get_vtask(vtid):
    global vtask_list
    return [x for x in vtask_list if x['vtid'] == vtid][0]

def executa_comando(name, vtid):
    global vtask_list
    l = [item for item in vtask_list if item['vtid'] == vtid]
    chdir(l[0]['name'])
    get = subprocess.Popen(name, shell=True, stdout=subprocess.PIPE)
    out = get.communicate()[0]
    chdir('../')
    return out

# Cria uma nova vtask
def vtask_new():
    global vtid
    global vtask_list
    vtid += 1
    name = str(time())+"vtask"
    dirname = getcwd()+"/"+name
    vtask_list.append({'vtid':vtid, 'name':name, 'dir':dirname})
    create = subprocess.Popen('virtualenv '+name, shell=True, stdout=subprocess.PIPE)
    out = create.communicate()
    return vtid

# Destroy uma vtask
def vtask_kill(vtid):
    global DIR
    global vtask_list
    l = [item for item in vtask_list if item['vtid'] == vtid]
    if len(l) > 0:
        vtask = l[0]
        # chdir(DIR)
        shutil.rmtree(vtask['name'])
        vtask_list.remove(vtask)

    return vtask

def show_dir():
    global basedir
    return basedir


server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

# registering functions to make a remote call
server.register_function(pow)
server.register_function(vtask_new)
server.register_function(vtask_kill)
server.register_function(executa_comando)
server.register_function(show_dir)
server.serve_forever()
