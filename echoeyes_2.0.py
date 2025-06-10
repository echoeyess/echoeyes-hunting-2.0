# Optimized Host Checker by EchoEyes - Upgraded with asyncio/aiohttp

import asyncio
import aiohttp
import os
import sys

# Terminal colors
orange, yellow, green, red, blue, cyan, white = '\033[38;5;208m', '\033[33m', '\033[32m', '\033[31m', '\033[34m', '\033[36m', '\033[37m'

async def fetch(session, url, expected_servers):
    try:
        async with session.get(f"https://{url}", timeout=10) as response:
            server = response.headers.get("Server", "").lower()
            status = response.status
            match = any(s.lower() in server for s in expected_servers)

            if status == 200 and match:
                print(f"{cyan}~ {green}[working] [{url}]{white}")
            else:
                print(f"{cyan}~ {orange}[N/W] [{url}]{white}")
    except Exception as e:
        print(f"{cyan}~ {red}[N/A] [{url}]{white}")

async def run_checker(hosts, expected_servers):
    connector = aiohttp.TCPConnector(limit=100)
    timeout = aiohttp.ClientTimeout(total=15)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }) as session:
        tasks = [fetch(session, host, expected_servers) for host in hosts]
        await asyncio.gather(*tasks, return_exceptions=True)

def main():
    try:
        os.system("clear")

        intro = f"""{red} 

            ⚠️ THIS TOOL IS FOR HUNTING PURPOSES ONLY                   
            ⚠️ MAKE SURE TO USE A SIM CARD WITH NO DATA      
            
            {yellow}Telegram account{white} -> {blue}@echoeyes{white}  
            {yellow}github{white} -> {blue}https://github.com/echoeyesdev{white}                                    
            
            {green}<----- let the Hunt begin ----->{white}
            coded with love by -->{blue}Echoeyes{white} <--
 
{blue}
choose index of the Server

[1] cloudflare 
[2] cloudfront 
[3] Apache
[4] HAProxy
[5] nginx all versions 
{white}
""" 
        print(intro)

        # Read hosts
        try:
            with open("hosts.txt", "r") as f:
                hosts = [h.strip() for h in f if h.strip()]
        except FileNotFoundError:
            print(f"{red}Error: 'hosts.txt' not found.{white}")
            sys.exit(1)

        # User input
        index = input("Choose the index of the server: ").strip()
        mapping = {
            "1": ["cloudflare"],
            "2": ["cloudfront", "amazons3"],
            "3": ["apache"],
            "4": ["haproxy"],
            "5": ["nginx"]
        }

        expected_servers = mapping.get(index)
        if not expected_servers:
            print(f"{red}Invalid choice.{white}")
            return

        print(f"{blue}You selected {green}{expected_servers[0].capitalize()}{blue}. Good luck!\n")
        asyncio.run(run_checker(hosts, expected_servers))

    except KeyboardInterrupt:
        print(f"\n{red}Scan interrupted by user. Exiting...{white}")
        sys.exit(0)
    except Exception as e:
        print(f"{red}Unexpected error: {e}{white}")
        sys.exit(1)

if __name__ == "__main__":
    main()