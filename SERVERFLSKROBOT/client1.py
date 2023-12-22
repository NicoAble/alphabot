#192.168.1.130
import time
import socket #nativa
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #costruttore --> con questa riga ho istanziato il socket (creazione del socket)
server_address = ('192.168.1.133', 3450) #192.168.0.123 indirizzo IP alphabot
s.connect(server_address)
print("connesso")

class receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection=s
    
    def run(self):
        while True:
            #print("thread is running")
            text_received, address = s.recvfrom(4096)
            text_received=text_received.decode()
            text=text_received.split(":")
            if text[0]=="0" and text[1]=="0":
                print("ostacolo DAVANTI")
            elif text[0]=="0" and text[1]=="1":
                print("ostacolo SINISTRA")
            elif text[0]=="1" and text[1]=="0":
                print("ostacolo DESTRA")
            time.sleep(1)

def main():
    ricevitore=receiver()
    ricevitore.start()
    while True:
        text = input("Scrivi il nome del comando(F, B, L, R, E): ")
        #print(text)
        
        text+= ";"+ input("inserisci la durata': ")+","+input("inserisci la velocità: ")
        s.sendto(text.encode(), server_address) #mando il messaggio al server
        
        text_received, address = s.recvfrom(4096)
        print(text_received.decode())
        if(text_received.decode()=="exit"): break
    ricevitore.join()
    s.close()


if __name__ == "__main__":
    main()