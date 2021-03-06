from xmlrpclib import ServerProxy
server = "http://localhost:8000" # define server address
s = ServerProxy(server)
print("Creating vtask....")
vtask_id = s.vtask_new()
print("Created vtask")
while True:
    cmd = raw_input("vtask:"+str(vtask_id)+"> ")
    if cmd == "exit":
        print("Destroying vtask...")
        print(s.vtask_kill(vtask_id))
        break

    if cmd == "dir":
        print(s.show_dir())
        continue
    
    print(s.executa_comando(cmd, vtask_id))
