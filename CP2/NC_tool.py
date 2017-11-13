#!/usr/bin/env python
# -*- coding utf-8 -*-

#import library
import sys
import socket
import getopt
import threading
import subprocess

#define variable
listen=False
command=False
upload=""
execute=""
target=""
upload_destination=""
port=0


#show banner
def banner():
    print "     #####      ##   #####                                        ##        "
    print "    ##  ##     ##   ##   ###        ##         ###        ###     ##        "
    print "   ##   ##    ##  ###      ##     ######     ##  ##    ##  ##    ##         "
    print "  ##    ##   ##  ###                ##      ##    ##  ##    ##  ##          "   
    print "  ##    ##  ##    ##      ##       ##  ##  ##     ## ##     ##  ##          "
    print " ##     ## ##     ##    ###        ##  ##   ##   ##   ##   ##  ##           "
    print " ##     ####       #####          #######    ####      ####    ##           "
    print ""
    #print ""
    #print ""
    print ""
    print "              ####   #####      ####     #####    ####     #####      ###   #####   ##     ##   "
    print "             #####  ##  ###    ##  ##   ##   ##  ##  ##    ##  ##   ## ##   ##  ##  ##    ##    " 
    print "            ##  ## ###        ## #  ## ##    ## ## #  ##  ######      ##   ######   ##   ##     "
    print "            ###### ###  ##### ##  # ## ##    ## ##  # ##  ##  ##      ##   ##  ##   ##  ##      "
    print "          ##    ##  ##  ## ##  ##  ## ##    ##   ##  ##  ##    ##    ##    ##   ##  ## ##       "
    print "          ##    ##   ####  ##   #### ########     ####   ##     ## ###### ##     ## ####        "
    print
    sys.exit(0)
    
#show how to use
def usage():
    print "NC tool"
    print "usage:BHC.py -t [target_host] -p [port]"
    print " -l --listen"
    print " -e --execute"
    print " -c --command"
    print " -u --upload"
    print 
    print 
    print
    print "-h --help       - show help"
    print "-ex --example   - show example"
    sys.exit(0)

#show sample use
def sample():
    print "sample case:"
    print "nc_tool.py -t 192.168.0.0 -p 9999 -l -c"
    print "nc_tool.py -t 192.168.0.0 -p 9999 -l -u c:\\target.exe"
    print "nc_tool.py -t 192.168.0.0 -p 9999 -l -e \"cat /etc/passwd\""
    print "echo 'ABCD' | ./nc_tool.py -t 192.168.0.0 -p 9999"
    print ""
    print ""
    sys.exit(0)

#main func
def main():
    
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    #no paramater
    if not len(sys.argv[1:]):
        usage()
    
    #proccess in command-line variable 
    try:
        opts, args=getopt.getopt(sys.argv[1:],
                                 "hsble:t:p:cu:b:",
                                 ["help","sample","banner","listen","execute=","target=","port=","command","upload="])
    
    #when error occur
    except getopt.GetoptError as err:
            print str(err)
            usage()
            
    for o,a in opts:
        
        if o in ("-h","--help"):
            usage()
        elif o in ("-s","--sample"):
            sample()
        elif o in ("-b","--banner"):
            banner()
        elif o in ("-l","--listen"):
            listen=True
        elif o in ("-e","--execute"):
            execute=a
        elif o in ("-c","--commandshell"):
            command=True
        elif o in ("-u","--upload"):
            upload_destination=a
        elif o in ("-t","--target"):
            target=a
        elif o in  ("-p","--port"):
            port=int(a)
        
        #Exception-handling
        else:
            assert False,"Unhandled Option"
        
        
    if not listen and len(target) and port > 0:
        buffer=sys.stdin.read()
        client_sender(buffer)
    
    #ready for connection
    if listen:
        server_loop()

def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        client.connect((target,port))
        
        if len(buffer):
            client.send(buffer)
            
            while True:
                recv_len=1
                response=""
                
                while recv_len:
                    data=client.recv(4096)
                    recv_len=len(data)
                    response+=data
                    
                    if recv_len<4096:
                        break
                    
                print response
                
                buffer=raw_input("")
                buffer+="\n"
                
                client.send(buffer)
                
    except:
        print "[*] Exception! Exiting. ..."    
        client.close()
        
def server_loop():
    global target
    
    #no IP_address -> stand by all interface
    if not len(target):
        target="0.0.0.0"
        
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    
    server.listen(5)
    
    while True:
        client_socket, addr =server.accept()
        
        client_thread=threading.Thread(
            target=client_handler,args=(client_socket,))
        client_thread.start()
        

def run_command(command):
    command=command.rstrip()
            
    try:
        command=command+"\n"
        output=subprocess.check_output(
        command,
        stderr=subprocess.STDOUT,
        shell=True
        )
        
    except:
            output="Failed to execute command\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    
    if len(upload_destination):
        file_buffer=""
        while True:
            data=client_sender/recv(1024)
            if len(data)==0:
                break
            else:
                file_buffer+=data
                
        try:
            file_descriptor=open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            cilent_socket.send(
            "Success"
            )
            
        except:
            client_socket.send(
            "Failed"
            )
            
    if len(execute):
        output=run_command(execute)
        
        client_socket.send(output)
        
    if command:
        prompt="<HOGE:#>"
        client_socket.send(prompt)
        
        while True:
            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
                
            response=run_command(cmd_buffer)
            response+=prompt
            client_socket.send(response)
            

main()