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


def SMTP(conn):
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
    time.sleep(2)



def openServer(port):
    print "open Unknown Server......port: "+str(port)+"\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))

    s.listen(1)
    conn, addr = s.accept()
    conn.setblocking(0)
    conn.settimeout(10)

    print 'Connected by', addr,"\n"

    try:
        SMTP(conn)
    except:
        conn.close()
        s.close()

        print 'Time out...\n'
        print "open Unknown Server......port: "+str(port+1)+"\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port+1))

        s.listen(1)
        conn, addr = s.accept()
        conn.setblocking(0)
        conn.settimeout(10)

        print 'Connected by', addr,"\n"

        print "Junk Data Send/Recv : 20 times\n"

        junk = "qfjkhdagfkjaIigsvxkjzvcqud5ufag5dfadqkjsdahUDTDJHGDKJHGDFKJFHGjhgfka5dgfa5jgfauiydguYgduygYGu7818943I1lI1vkjhgkfJHFDRDHGCHJrYTFF11GKJGHTDJHGDKJHGDn(JFHGjhgfkasdgfasjqfauiyd5UYGIUYIDYGI769381276g\n"
        for i in range(20):
          data = conn.recv(1024) #client_to_server : junk
          print client_to_server+data+"\n"

          print server_to_client+junk
          conn.send(junk)

	time.sleep(2)
        SMTP(conn)

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
