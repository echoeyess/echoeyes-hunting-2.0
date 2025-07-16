# 10x faster with clean output 

# Telegram: @EchoEyesOfficial | GitHub: https://github.com/echoeyess

import asyncio
import aiohttp
import os
import sys
import dns.resolver
from tqdm import tqdm

# Termux Colors
orange, yellow, green, red, blue, cyan, white = '\033[38;5;208m', '\033[33m', '\033[32m', '\033[31m', '\033[34m', '\033[36m', '\033[37m'

SEM = asyncio.Semaphore(100)
CDN_SIGNATURES = [
    "cloudflare", "akamai", "cloudfront", "fastly", "incapsula", "stackpath",
    "netdna", "cachefly", "edgesuite", "edgekey", "azureedge", "google", "gws",
    "cdngc", "vercel", "hwcdn", "cdn77", "cdnsun", "quantil"
]

progress_bar = None
working_hosts = []
print_lock = asyncio.Lock()

def detect_cdn(host, server_header):
    try:
        if any(cdn in server_header for cdn in CDN_SIGNATURES):
            return True
        answers = dns.resolver.resolve(host, 'CNAME')
        for rdata in answers:
            cname = str(rdata.target).lower()
            if any(cdn in cname for cdn in CDN_SIGNATURES):
                return True
    except:
        pass
    return False

async def fetch(session, url, expected_servers):
    global progress_bar
    async with SEM:
        try:
            async with session.get(f"https://{url}", timeout=10, ssl=False) as response:
                status = response.status
                server = response.headers.get("Server", "").lower().split("/")[0].strip()
                cdn_status = "[CDN Detected]" if detect_cdn(url, server) else "[No CDN]"

                if status == 200:
                    if any(s.lower() in server for s in expected_servers):
                        async with print_lock:
                            tqdm.write(f"{cyan}~ {green}[WORKING] 200 OK [{url}] → {server} {yellow}{cdn_status}{white}")
                        working_hosts.append(url)
                    else:
                        async with print_lock:
                            tqdm.write(f"{cyan}~ {yellow}[WRONG SERVER] 200 OK [{url}] → {server or 'unknown'} {yellow}{cdn_status}{white}")
        except:
            pass
        finally:
            async with print_lock:
                progress_bar.update(1)

async def run_checker(hosts, expected_servers):
    global progress_bar
    timeout = aiohttp.ClientTimeout(total=15)
    connector = aiohttp.TCPConnector(limit=100, ssl=False)

    progress_bar = tqdm(total=len(hosts), desc="Checking", colour="cyan", ncols=75, leave=True, dynamic_ncols=True)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector, headers={
        "User-Agent": "Mozilla/5.0 (EchoEyes Host Checker)"
    }) as session:
        tasks = [fetch(session, host, expected_servers) for host in hosts]
        await asyncio.gather(*tasks)
    progress_bar.close()

def main():
    try:
        os.system("clear" if os.name != "nt" else "cls")

        print(f"""{cyan}
▄███▄   ▄█▄     ▄  █ ████▄ ▄███▄ ▀▄    ▄ ▄███▄     ▄▄▄▄▄   
█▀   ▀  █▀ ▀▄  █   █ █   █ █▀   ▀  █  █  █▀   ▀   █     ▀▄ 
██▄▄    █   ▀  ██▀▀█ █   █ ██▄▄     ▀█   ██▄▄   ▄  ▀▀▀▀▄   
█▄   ▄▀ █▄  ▄▀ █   █ ▀████ █▄   ▄▀  █    █▄   ▄▀ ▀▄▄▄▄▀    
▀███▀   ▀███▀     █        ▀███▀  ▄▀     ▀███▀             
                 ▀                                         
{white}""")

        print(f"""{cyan}
┌────────────────────────────────────────────────────────────┐
│{yellow}                EchoEyes Host Checker                {cyan}│
├────────────────────────────────────────────────────────────┤
│ {white}GitHub:    {blue}https://github.com/echoeyess{cyan}                   │
│ {white}Telegram:  {blue}@echoeyess{cyan}                                    │
│ {white}Created by:{blue} EchoEyes{cyan}                                      │
└────────────────────────────────────────────────────────────┘
{white}""")

        print(f"""{blue}Choose a server type to match:

[1] Cloudflare
[2] Cloudfront
[3] Apache
[4] HAProxy
[5] Nginx
[6] Microsoft Azure/IIS
[7] LiteSpeed
[8] Google Frontend
[9] Amazon EC2/AWS
[10] DigitalOcean
[11] Fastly CDN
[12] Akamai CDN
[13] Tencent Cloud
[14] Baidu CDN
[15] Custom Server Name
{white}
""")

        try:
            with open("all_domains.txt", "r") as file:
                hosts = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"{red}Error: 'all_domains.txt' not found.{white}")
            sys.exit(1)

        if not hosts:
            print(f"{red}No hosts found in 'all_domains.txt'.{white}")
            return

        index = input(f"{yellow}Enter the index of the server: {white}").strip()
        mapping = {
            "1": ["cloudflare"],
            "2": ["cloudfront", "amazons3"],
            "3": ["apache"],
            "4": ["haproxy"],
            "5": ["nginx"],
            "6": ["microsoft-iis", "azure", "microsoft"],
            "7": ["litespeed"],
            "8": ["gws", "google", "google frontend"],
            "9": ["amazon", "awselb", "ec2"],
            "10": ["digitalocean"],
            "11": ["fastly"],
            "12": ["akamai", "akamaighost"],
            "13": ["tencent"],
            "14": ["baidu"],
            "15": ["custom"]
        }

        expected_servers = mapping.get(index)
        if not expected_servers:
            print(f"{red}Invalid choice.{white}")
            return

        if expected_servers == ["custom"]:
            custom = input(f"{yellow}Enter custom server name to match: {white}").strip().lower()
            if not custom:
                print(f"{red}Custom server name cannot be empty.{white}")
                return
            expected_servers = [custom]

        print(f"\n{blue}✔ You selected: {green}{', '.join(expected_servers)}{white}\n")
        asyncio.run(run_checker(hosts, expected_servers))

        # Save working hosts
        with open("working_hosts.txt", "w") as f:
            for host in working_hosts:
                f.write(host + "\n")

        print(f"\n{green}✔ Done! Saved working hosts to 'working_hosts.txt'{white}")

    except KeyboardInterrupt:
        print(f"\n{red}Scan interrupted by user. Exiting...{white}")
        sys.exit(0)
    except Exception as e:
        print(f"{red}Unexpected error: {e}{white}")
        sys.exit(1)

if __name__ == "__main__":
    main()