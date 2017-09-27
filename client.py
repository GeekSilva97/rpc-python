from xmlrpclib import ServerProxy
server = "http://localhost:8000"
s = ServerProxy(server)
print("Creating vtask....")
vtask_id = s.vtask_new()
print("Created vtask")
while True:
    cmd = raw_input("vtask:"+str(vtask_id)+"> ")
    print(s.executa_comando(cmd))
    if cmd == "exit":
        print("Destroying vtask...")
        s.vtask_kill(vtask_id)
        break
