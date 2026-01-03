# Case Law Scraper – Coding Challenge

## Problem Summary

The goal of this project is to scrape case law data from  
**The National Archives – Find Case Law** website.

Specificallly, we are required to:
- Scrape the **first three pages** of the case law search results
- Collect **metadata** for each case:
  - Title
  - Court name
  - Citation(s)
  - Date
  - Case URL
- Visit each case page and extract the **raw judgment text**
  (plain text with no HTML or markup)
- Store the final result in a **Pandas DataFrame**

Bonus tasks include:
- Extracting **PDF and XML links** from each case page
- Converting PDFs into HTML

---

## Approach

The problem was solved in two main steps:

### 1. Scraping the Lister Pages
- The search results pages are paginated using query parameters (`page=1`, `page=2`, etc.).
- A loop is used to scrape the **first three pages**, making it easy to extend to all pages later.
- From each lister page, basic case metadata and the case URL are extracted.

### 2. Scraping Individual Case Pages
- Each case URL collected from the lister pages is visited.
- The judgment content is extracted and converted to **raw text** by removing all HTML tags.
- Additional links to **PDF and XML files** are captured where available.

---

## Output

- All collected data is stored in a **Pandas DataFrame**
- Each row represents a single case with its metadata and judgment text
- The structure is suitable for further analysis or storage

---

## Tools Used

- Python
- `requests` for HTTP requests
- `BeautifulSoup` for HTML parsing
- `pandas` for data storage and processing

---

## Notes

- The scraper is designed to be **clean, modular, and scalable**
- Functions are separated for fetching pages, parsing lister pages, and parsing case pages
- Polite scraping practices (headers, pagination control) are followed
