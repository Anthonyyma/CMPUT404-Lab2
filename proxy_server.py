#code based on lab code
import socket
from multiprocessing import Process

#define buffer size
BUFFER_SIZE = 1024

def main():
    host = "www.google.com"
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyStart:
        print("Starting proxy server")
        #allow reused addresses, bind, and set to listening mode
        proxyStart.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxyStart.bind((host, port))
        proxyStart.listen(1)
    
        #continuously listen for connections
        while True:
            conn, addr = proxyStart.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyEnd:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                #connect proxy end
                proxyEnd.connect((remote_ip, port))

                #initialize Process
                p = Process(target=handle_proxy, args=(addr, conn))
                p.daemon = True
                p.start()
                print("Started process", p)
    
            conn.close()

def handle_proxy(addr, conn):
    #send data
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)

    #shut down
    conn.shutdown(socket.SHUT_WR)

    data = conn.recv(BUFFER_SIZE)

    #send data back
    conn.send(data)
            

if __name__ == "__main__":
    main()
