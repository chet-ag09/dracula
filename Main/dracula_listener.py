import socket


def listener(ip, port):
    port = int(port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    
    client, addr = server.accept()
    print(f"[-] Connection received from {addr[0]}:{addr[1]} !!!")
    
    client.sendall(b"pwd\n")
    prompt = client.recv(1024).decode(errors='ignore').strip() + " >>> "

    
    while True:
        try:
            cmd = input("\033[0;32m"+prompt+"\033[0m")
            if not cmd:
                continue
            elif cmd.lower() in ["exit", "quit"]:
                print("[-] Closing connection...")
                client.sendall(b"exit\n")
                break
            
            client.sendall(cmd.encode() + b"\n")
            
            output = ""
            while True:
                chunk = client.recv(1024).decode(errors='ignore')
                if not chunk:
                    break
                output += chunk
                if output.endswith("\n"):
                    break
            
            lines = output.split("\n")
            
            client.sendall(b"pwd\n")
            prompt = client.recv(1024).decode(errors='ignore').strip() + " >>> "
            
            print("\n".join(lines[:-2]))
        except Exception as e:
            print(f"[!] Error: {e}")
            break
    
    client.close()
    server.close()
    print("[-] Listener stopped.")