
# **EchoEyes Tool Usage Guide**

Welcome to the **EchoEyes Multi-Tool Project** — a powerful toolkit for **freenet explorers, tunnel testers, and freedom hackers**.

---

## **1. EchoEyes Host Checker (Accurate Mode)**

**Purpose:**  
Check a list of hosts and verify if they are working and match a specific server type (Cloudflare, Cloudfront, Nginx, etc).

**How to Use:**  
1. Create a file named `hosts.txt` in the same folder containing one hostname per line.  
2. Run `echoeyes_2.0.py` script  
3. Choose the server type you want to match from the menu.  
4. The tool will test each host and print results:  
   - `[working]` if status 200 and server matches your choice  
   - `[WRONG SERVER]` if status 200 but server does not match  
   - Errors like Timeout or Connection Error if unreachable

---

## **2. EchoEyes URL Extractor**

**Purpose:**  
Extract clean domain names from junk text, websites, or PDF files.

**How to Use:**  
1. Run the URL Extractor script.  
2. Choose input source:  
   - `[1]` Extract from a Website URL  
   - `[2]` Extract from a Text File (default: `junk.txt`)  
   - `[3]` Extract from a PDF File  
3. Input the URL or file path as prompted.  
4. The script extracts and prints clean domains, saving them to `hosts.txt`.

---

## **Requirements**

Install required Python libraries with: 
pip install -r requirements

---

## **Tips**

- Clean your input files for better extraction results.  
- Use the output `hosts.txt` from the Extractor as input for the Host Checker.

---

## **Creator**

Made with ♥ by EchoEyes  
Telegram: @echoeyess  
GitHub: https://github.com/echoeyess
