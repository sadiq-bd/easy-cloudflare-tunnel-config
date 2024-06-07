# Easy Cloudflare Tunnel Config
Makes Tunnel Configuration more readable and easier

## Usage
1. Edit tunnel.list and put tunnel id, credentials file in tunnel-update.py

2. just one command
   
<code>python3 tunnel-update.py</code>

3. If you want to restart cloudflared service automatically

<code>sudo python3 tunnel-update.py --restart</code>

