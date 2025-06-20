# EchoEyes Host Checker
# With Added Server List 
# 10x faster than before

# Telegram account @echoeyess
# github: https://github.com/echoeyess

import asyncio
import aiohttp
import os
import sys

orange, yellow, green, red, blue, cyan, white = '\033[38;5;208m', '\033[33m', '\033[32m', '\033[31m', '\033[34m', '\033[36m', '\033[37m'

SEM = asyncio.Semaphore(100)

async def fetch(session, url, expected_servers):
    async with SEM:
        try:
            async with session.get(f"https://{url}", timeout=10, ssl=False) as response:
                status = response.status
                server = response.headers.get("Server", "").lower().split("/")[0].strip()

                if status == 200:
                    if any(s.lower() in server for s in expected_servers):
                        print(f"{cyan}~ {green}[working] 200 OK [{url}] → {server}{white}")
                    else:
                        print(f"{cyan}~ {yellow}[WRONG SERVER] 200 OK [{url}] → {server or 'unknown'}{white}")
                else:
                    print(f"{cyan}~ {orange}[NOT 200] [{url}] → status: {status}, server: {server or 'unknown'}{white}")

        except asyncio.TimeoutError:
            print(f"{cyan}~ {red}[Timeout] [{url}]{white}")
        except aiohttp.ClientConnectorError:
            print(f"{cyan}~ {red}[Connection Error] [{url}]{white}")
        except Exception as e:
            print(f"{cyan}~ {red}[Error: {str(e)}] [{url}]{white}")

async def run_checker(hosts, expected_servers):
    timeout = aiohttp.ClientTimeout(total=15)
    connector = aiohttp.TCPConnector(limit=100, ssl=False)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector, headers={
        "User-Agent": "Mozilla/5.0 (EchoEyes Host Checker)"
    }) as session:
        tasks = [fetch(session, host, expected_servers) for host in hosts]
        await asyncio.gather(*tasks)

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
            with open("hosts.txt", "r") as file:
                hosts = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"{red}Error: 'hosts.txt' not found.{white}")
            sys.exit(1)

        if not hosts:
            print(f"{red}No hosts found in 'hosts.txt'.{white}")
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

    except KeyboardInterrupt:
        print(f"\n{red}Scan interrupted by user. Exiting...{white}")
        sys.exit(0)
    except Exception as e:
        print(f"{red}Unexpected error: {e}{white}")
        sys.exit(1)

if __name__ == "__main__":
    main()
