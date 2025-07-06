# bruteTGT

A minimal Python tool for brute-forcing valid Kerberos credentials by requesting TGTs via Impacket's `impacket-getTGT`.

---

## Features

- Uses Impacket’s `impacket-getTGT` script directly
- Brute-forces user/password combinations
- Detects:
  - ✅ Valid credentials
  - ❌ Invalid credentials
  - 🚫 Revoked accounts
  - 🕒 Timeouts / unknown errors
- Color-coded CLI output
- Easy CLI interface with argument parsing

---

## Requirements

- Python 3.7+
- [Impacket](https://github.com/fortra/impacket)

Install dependencies:

```bash
pip install impacket
```

## Usage
```bash
python3 bruteTGT.py -d <domain> --dc-ip <ip> -u <userlist> -p <passlist>
```
