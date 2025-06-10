import re
import requests
from bs4 import BeautifulSoup
import PyPDF2  # NEW for PDF extraction

def extract_visible_text_from_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"❌ Error fetching website: {e}")
        return ""

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
    return text

def extract_clean_websites_from_text(text):
    pattern = re.compile(r"\b(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?\b")
    matches = re.findall(pattern, text)

    clean_sites = set()
    for match in matches:
        clean = match.strip().lower().split('/')[0].split('?')[0].split('#')[0]
        clean_sites.add(clean)

    return sorted(list(clean_sites))

def save_to_txt(data, filename="websites_only.txt"):
    with open(filename, "w") as f:
        pass  # clear file first
    with open(filename, "w") as f:
        for site in data:
            f.write(site + "\n")
    print(f"\n✅ Saved {len(data)} website(s) to '{filename}'")

def main():
    choice = input("Type 'text' for junky text, 'website' for website URL, or 'pdf' for a PDF file: ").strip().lower()

    if choice == "text":
        print("\n📝 Paste your junky paragraph text below:")
        user_text = input()
        websites = extract_clean_websites_from_text(user_text)

    elif choice == "website":
        site = input("🌐 Enter website URL (e.g., www.vodacom.co.za): ").strip()
        visible_text = extract_visible_text_from_website(site)
        websites = extract_clean_websites_from_text(visible_text)

    elif choice == "pdf":
        file_path = input("📄 Enter full path to your PDF file (e.g., myfile.pdf): ").strip()
        pdf_text = extract_text_from_pdf(file_path)
        websites = extract_clean_websites_from_text(pdf_text)

    else:
        print("❌ Invalid choice.")
        return

    if websites:
        print("\n🌍 Websites found:")
        for site in websites:
            print(site)
        save_to_txt(websites)
    else:
        print("❌ No websites found.")
        open("websites_only.txt", "w").close()

if __name__ == "__main__":
    main()