# EchoEyes Url extractor

# Telegram account @EchoEyesOfficial
# github: https://github.com/echoeyess


import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import PyPDF2
import os
import urllib3

os.system("")

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


orange = '\033[38;5;208m'
yellow = '\033[33m'
green = '\033[32m'
red = '\033[31m'
blue = '\033[34m'
cyan = '\033[36m'
white = '\033[0m'

# Extract visible text from a website
def extract_visible_text_from_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        response = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"{red}Error fetching website: {e}{white}")
        return ""

# Extract text from PDF file
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"{red}Error reading PDF: {e}{white}")
    return text

# Extract clean domains from text
def extract_clean_websites_from_text(text):
    pattern = re.compile(r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?(?:/[^\s]*)?\b')
    matches = re.findall(pattern, text)
    clean_sites = set()

    for match in matches:
        parsed = urlparse(match if match.startswith("http") else "http://" + match)
        domain = parsed.netloc.lower()
        if domain:
            clean_sites.add(domain)

    return sorted(clean_sites)

# Save domains to hosts.txt
def save_to_hosts(data, filename="hosts.txt"):
    full_path = os.path.abspath(filename)
    with open(full_path, "w") as f:
        for site in data:
            f.write(site.strip() + "\n")
    print(f"\n{green}✅ Saved {len(data)} website(s) to:{white} {blue}{full_path}{white}")

# Main logic
def main():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""
{orange}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     ECHOEYES DOMAIN EXTRACTOR      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{white}

{cyan}Extract clean domain names from junk, websites or PDFs.{white}

{blue}[1]{white} Extract from a Website URL
{blue}[2]{white} Extract from a Text File (default: junk.txt)
{blue}[3]{white} Extract from a PDF File
""")

    choice = input(f"{yellow}Select an option: {white}").strip()

    if choice == "1":
        site = input(f"{yellow}Enter website URL: {white}").strip()
        visible_text = extract_visible_text_from_website(site)
        websites = extract_clean_websites_from_text(visible_text)

    elif choice == "2":
        filepath = input(f"{yellow}Enter text file path (default: junk.txt): {white}").strip()
        if filepath == "":
            filepath = "junk.txt"
        if not os.path.exists(filepath):
            print(f"{red}❌ File not found: {filepath}{white}")
            return
        with open(filepath, "r", encoding="utf-8") as f:
            user_text = f.read()
        websites = extract_clean_websites_from_text(user_text)

    elif choice == "3":
        pdf_path = input(f"{yellow}Enter PDF file path: {white}").strip()
        if not os.path.exists(pdf_path):
            print(f"{red}❌ File not found: {pdf_path}{white}")
            return
        pdf_text = extract_text_from_pdf(pdf_path)
        websites = extract_clean_websites_from_text(pdf_text)

    else:
        print(f"{red}❌ Invalid option.{white}")
        return

    if websites:
        print(f"\n{green}Extracted websites:{white}")
        for site in websites:
            print(site)
        save_to_hosts(websites)
    else:
        print(f"{orange}⚠️ No websites found in the input.{white}")
        open("hosts.txt", "w").close()

if __name__ == "__main__":
    main()
