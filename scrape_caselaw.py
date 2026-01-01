import requests
from bs4 import BeautifulSoup
import pandas as pd
import fitz  # PyMuPDF
import time

# Constants
BASE_URL = "https://caselaw.nationalarchives.gov.uk"
SEARCH_URL = f"{BASE_URL}/judgments/search?query="

def get_case_details(case_url):
    """Visits the case page to get Raw Text and PDF/XML links."""
    try:
        response = requests.get(case_url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # 1. Raw Text Extraction (No HTML tags)
        judgment_body = soup.find("div", class_="judgment-body") or soup.find("article")
        raw_text = judgment_body.get_text(separator="\n", strip=True) if judgment_body else "N/A"

        # 2. PDF/XML Link Extraction
        pdf_link, xml_link = "N/A", "N/A"
        links = soup.find_all("a", href=True)
        for l in links:
            href = l['href']
            if ".pdf" in href.lower(): pdf_link = BASE_URL + href if href.startswith('/') else href
            if ".xml" in href.lower(): xml_link = BASE_URL + href if href.startswith('/') else href

        return raw_text, pdf_link, xml_link
    except:
        return "Error", "N/A", "N/A"

def pdf_to_html(pdf_url):
    """Bonus: Processes PDF bytes into HTML strings."""
    if not pdf_url or pdf_url == "N/A": return "N/A"
    try:
        res = requests.get(pdf_url, timeout=10)
        doc = fitz.open(stream=res.content, filetype="pdf")
        return "".join([page.get_text("html") for page in doc])
    except:
        return "Conversion Error"

def main():
    all_data = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    for page in range(1, 4):  # Requirement: First 3 pages
        print(f"Scraping Page {page}...")
        response = requests.get(f"{SEARCH_URL}&page={page}", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Based on your diagnostic, we look for table rows <tr>
        rows = soup.find_all("tr")
        
        for row in rows:
            # We look for the link inside the title div you found
            title_div = row.find("div", class_="judgments-table__title")
            if not title_div: continue
            
            link_tag = title_div.find("a")
            if not link_tag: continue

            case_url = BASE_URL + link_tag['href']
            print(f"  Processing: {link_tag.get_text(strip=True)[:50]}...")

            # Metadata Extraction from the row
            # Usually, Court and Date are in neighboring <td> or <span> tags
            court = row.find("span", class_="judgments-table__court")
            citation = row.find("span", class_="judgments-table__neutral-citation")
            date = row.find("time")

            # Fetch deep details
            raw_text, pdf_link, xml_link = get_case_details(case_url)
            
            all_data.append({
                "title": link_tag.get_text(strip=True),
                "court_name": court.get_text(strip=True) if court else "N/A",
                "citations": citation.get_text(strip=True) if citation else "N/A",
                "dates": date.get_text(strip=True) if date else "N/A",
                "url": case_url,
                "raw_text": raw_text,
                "pdf_link": pdf_link,
                "xml_link": xml_link,
                "pdf_as_html": pdf_to_html(pdf_link)
            })
            time.sleep(0.3) # Polite scraping delay

    # Create Final Dataframe
    df = pd.DataFrame(all_data)
    df.to_csv("moonlit_results.csv", index=False)
    print(f"\nSuccess! Saved {len(df)} cases to moonlit_results.csv")
    return df

if __name__ == "__main__":
    main()