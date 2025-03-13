WIP, HASNT PROPERLY BEEN TESTED ON OTHER SYSTEMS
works as of now
# Dracula 

Dracula is a Python-based tool designed to generate reverse shell payloads using PowerShell and Command Prompt. It provides options to create encoded payloads for stealth and supports direct connection to a target system once the payload is executed.

## Features
- Generates PowerShell-based reverse shell payloads
- Supports both plain text and Base64 encoded payloads
- Allows automatic connection to a target after execution



## Installation
Ensure you have Python installed, then clone this repository:

```bash
git clone https://github.com/chet-ag09/dracula
cd dracula
```

Install any necessary dependencies:

```bash
pip install -r requirements.txt  
```

## Usage
Run the script using:

```bash
python dracula.py
```

### Commands

- **Generate a reverse shell payload:**
  ```bash
  Dracula >> -IP <attacker-ip> -PORT <port> -OUTFILE <output-file>
  ```

- **Generate an encoded payload (Base64):**
  ```bash
  Dracula >> -IP <attacker-ip> -PORT <port> -OUTFILE <output-file> -ENCODED
  ```

- **Display payload directly:**
  ```bash
  Dracula >> -IP <attacker-ip> -PORT <port>
  ```

- **Display an encoded payload:**
  ```bash
  Dracula >> -IP <attacker-ip> -PORT <port> -ENCODED
  ```

- **Start a listener after payload execution:**
  ```bash
  Dracula >> -IP <attacker-ip> -PORT <port> -CONNECT
  ```

## Example

To generate a Base64 encoded payload for a reverse shell:

```bash
Dracula >> -IP 192.168.1.10 -PORT 4444 -OUTFILE shell.bat -ENCODED
```

To start a listener after the payload is executed:

```bash
Dracula >> -IP 192.168.1.10 -PORT 4444 -CONNECT
```

## Disclaimer
This tool is intended for educational and ethical penetration testing purposes only. The author does not take responsibility for any misuse. Use this tool only on systems you own or have explicit permission to test.

