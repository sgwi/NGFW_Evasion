#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     29-10-2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket, getopt, sys, time

client_to_server = """(Client-to-Server)\n"""
server_to_client = """(Server-to-Client)\n"""

def HTTP_Response(conn):

    http_response="HTTP/1.1 200 OK\r\n\r\n"

    print server_to_client+http_response
    conn.send(http_response)


def SMTP(conn):

    print server_to_client+"220 mail.test_NGFW.org Mail Service\n"
    conn.send("220 mail.test_NGFW.org Mail Service\n")

    time.sleep(2)
    data= conn.recv(1024) # client to server : helo
    print client_to_server+data


    print server_to_client+"250 Hello mail.test_NGFW.org\n"
    conn.send("250 Hello mail.test_NGFW.org\n")

    time.sleep(2)
    data= conn.recv(1024) # client to server : MAIL FROM:<user@test_NGFW.org>
    print client_to_server+data


    print server_to_client+"250 OK\n"
    conn.send("250 OK\n")


    time.sleep(2)
    data = conn.recv(1024) # client to server : RCPT TO:<user2@test_NGFW.org>
    print client_to_server+data

    print server_to_client+"250 OK\n"
    conn.send("250 OK\n")

    time.sleep(2)
    data = conn.recv(1024) # client to server : DATA
    print client_to_server+data

    print server_to_client+"354 End data with <CR><LF>.<CR><LF>\n"
    conn.send("354 End data with <CR><LF>.<CR><LF>\n")

    time.sleep(2)
    data = conn.recv(1024) # client to server : Test Data...
    print client_to_server+data

    print server_to_client+"250 OK\n"
    conn.send("250 OK\n")

    time.sleep(2)
    data = conn.recv(1024) # client to server : QUIT
    print client_to_server+data

    print server_to_client+"221 Bye\n"
    conn.send("221 Bye\n")
    time.sleep(5)



def openServer(port):
    print "open Collusion Server......port: "+str(port)+"\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))

    s.listen(1)
    conn, addr = s.accept()
    conn.setblocking(0)
    conn.settimeout(10)


    print 'Connected by', addr,"\n"

    try:
        SMTP(conn)
	time.sleep(2)
    except:
	conn.close()
	s.close()

	print 'Time out...\n'
	print "open Switching Server......port: "+str(port+1)+"\n"
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.bind(('', port+1))
	#s.bind(('', 80))

    	s.listen(1)
    	conn, addr = s.accept()
    	conn.setblocking(0)
    	conn.settimeout(10)

        for i in range(20):
            data = conn.recv(135) #client_to_server : http_request
            print client_to_server+data+"\n"

            HTTP_Response(conn)

        time.sleep(2)
        SMTP(conn)
	time.sleep(3)

    conn.close()

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:],"p:h",["port="])
    if(len(opts)==0):
      print 'server.py -p <port>'
      sys.exit()

    for opt, arg in opts:
      if opt == '-h':
         print 'server.py -p <port>'
         sys.exit()
      elif opt in ("-p", "--port"):
         port = arg
         openServer(int(port))
