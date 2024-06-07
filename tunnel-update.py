import os
import subprocess
import argparse

TUNNEL_ID = 'tunnel_id_here'
CREDENTIALS_FILE = '/root/.cloudflared/tunnel_id_here.json'

TUNNEL_FILE = 'tunnel.list'
ORIGINAL_CONFIG_FILE = '/etc/cloudflared/config.yml'

DEFAULT_SERVICE = 'http_status:404' # if exists on tunnel list then it will be ignored

ENTRY_DELIMITER = '@'

def generate_config(tunnel_file, config_file):
    with open(tunnel_file, 'r') as f:
        tunnel_entries = f.readlines()

    with open(config_file, 'w') as f:
        f.write("tunnel: " + TUNNEL_ID + "\n")
        f.write("credentials-file: " + CREDENTIALS_FILE + "\n")
        f.write("\n")
        f.write("ingress:\n")

        default_written = False

        for entry in tunnel_entries:
            entry = entry.strip()
            
            # skip blank lines and comments
            if entry == '' or entry.startswith('#'):
                continue

            parts = entry.split(ENTRY_DELIMITER)

            if len(parts) >= 2:

                origin, hostname = parts[0].strip(), parts[1].strip()
                
                for host in hostname.split(','):
                    f.write(f"  - hostname: {host.strip()}\n")
                    f.write(f"    service: {origin}\n")
                    
                    # origin rule 
                    if len(parts) >= 3:
                        f.write(f"    originRequest:\n")
                        originRule = parts[2].strip()
                        if ',' in originRule:
                            for rule in originRule.split(','):
                                f.write(f"      {rule.strip()}\n")
                        else:
                            f.write(f"      {originRule}\n")

                f.write("\n")

            else:
                # default
                f.write(f"  - service: {entry}\n")
                default_written = True

        if not default_written:
            f.write(f"  - service: {DEFAULT_SERVICE}\n")

def restart_cloudflared():
    print("Restarting Cloudflared...")
    subprocess.Popen(["systemctl", "restart", "cloudflared.service"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Cloudflared Tunnel Configuration")
    parser.add_argument('--restart', action='store_true', help='Restart Cloudflared after generating the config')
    args = parser.parse_args()

    generate_config(TUNNEL_FILE, ORIGINAL_CONFIG_FILE)

    # Check if restart is requested
    if args.restart:
        restart_cloudflared()

