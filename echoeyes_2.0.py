# EchoEyes The Goat !!

# 10x faster 
# New Domain Fetcher Feature
# Clean Output Bruu 

# Telegram: @EchoEyesOffcial
# GitHub: https://github.com/echoeyess

import asyncio
import aiohttp
import os
import sys
import dns.resolver
import requests
import threading
import time
from tqdm import tqdm

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

def spinner(stop_event):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rFetching domains... {symbols[i % len(symbols)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write("\rFetching domains... Done!\n")

def fetch_domains(tld, max_retries=3):
    clean_tld = tld.lstrip(".").lower()
    url = f"https://crt.sh/?q=%.{clean_tld}&output=json"
    stop_event = threading.Event()
    thread = threading.Thread(target=spinner, args=(stop_event,))
    thread.start()

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Unexpected response code: {response.status_code}")
            data = response.json()
            domains = set()

            for entry in data:
                name_value = entry.get("name_value", "")
                for name in name_value.splitlines():
                    clean_name = name.lower().lstrip("*.").strip()
                    if clean_name.endswith(f".{clean_tld}"):
                        domains.add(clean_name)

            stop_event.set()
            thread.join()

            if not domains:
                print("[-] No domains found.")
                return False

            with open("all_domains.txt", "w") as file:
                file.write("\n".join(sorted(domains)))

            print(f"[✓] Saved {len(domains)} domains to: all_domains.txt")
            return True

        except Exception as e:
            if attempt == max_retries:
                stop_event.set()
                thread.join()
                print(f"[-] Error after {max_retries} attempts: {e}")
                return False
            else:
                print(f"[!] Attempt {attempt} failed. Retrying...")

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

def show_domain_adder_page():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{cyan}
┌────────────────────────────────────────────────────────────┐
│{yellow}             EchoEyes Domain Fetcher            {cyan}│
└────────────────────────────────────────────────────────────┘
{white}""")
    tld = input(f"{yellow}~ Enter the domain suffix (e.g. gov.za): {white}").strip().lower()
    if tld:
        success = fetch_domains(tld)
        if success:
            print(f"{green}[✓] Successfully added hosts ending with .{tld}{white}")
        else:
            print(f"{red}[-] Failed to fetch or save domains for .{tld}{white}")
    else:
        print(f"{red}[-] Invalid TLD input.{white}")
    input(f"\n{blue}Press Enter to continue to scan page...{white}")
    os.system("clear" if os.name != "nt" else "cls")

def scan_main():
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
│ {white}Telegram:  {blue}@EchoEyesOffcial{cyan}                                    │
│ {white}Coded by:{blue} EchoEyes{cyan}                                      │
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

def main():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{cyan}
┌────────────────────────────────────────────────────────────┐
│{yellow}                EchoEyes Domain Fetcher               {cyan}│
└────────────────────────────────────────────────────────────┘
{white}""")
    print(f"{blue}[1] Add new domains | {red}Data Required{blue}")
    print(f"{blue}[2] Proceed to scan")
    choice = input(f"\n{yellow}Enter your choice: {white}").strip()

    if choice == "1":
        show_domain_adder_page()
        scan_main()
    elif choice == "2":
        scan_main()
    else:
        print(f"{red}Invalid choice.{white}")

if __name__ == "__main__":
    main()