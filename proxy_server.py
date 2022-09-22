#code based on lab code
import socket
import time
import sys
from multiprocessing import Process

#define buffer size, host, port
BUFFER_SIZE = 1024
HOST = "127.0.0.1"
PORT = 8001

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print(socket.error)
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    proxyHost = "www.google.com"
    proxyPort = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyStart:
        print("Starting proxy server")
        #allow reused addresses, bind, and set to listening mode
        proxyStart.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxyStart.bind((HOST, PORT))
        proxyStart.listen(1)
    
        #continuously listen for connections
        while True:
            conn, addr = proxyStart.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyEnd:
                print("Connecting to Google")
                remote_ip = get_remote_ip(proxyHost)

                #connect proxy end
                proxyEnd.connect((remote_ip, proxyPort))
                #initialize Process
                p = Process(target=handle_proxy, args=(conn, proxyEnd))
                p.daemon = True
                p.start()
                print("Started process", p)
    
            conn.close()

def handle_proxy(conn, proxyEnd):
    #send data
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    proxyEnd.sendall(full_data)
    #receive response
    data = proxyEnd.recv(BUFFER_SIZE)
    #send data back
    send_data(conn, data)
            
if __name__ == "__main__":
    main()
