import requests
import os
import time
from urllib.parse import urlparse, urljoin
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from src.config import TARGET_WEBSITES, RAW_DATA_DIR, USER_AGENT, REQUEST_TIMEOUT

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_domain_name(url):
    return urlparse(url).netloc.replace("www.", "")

def save_raw_html(content, domain, page_type, timestamp):
    """Saves raw HTML content to a file structure."""
    directory = os.path.join(RAW_DATA_DIR, domain, timestamp)
    os.makedirs(directory, exist_ok=True)
    
    filename = f"{page_type}.html"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    logger.info(f"Saved {page_type} for {domain} at {filepath}")
    return filepath

def fetch_url(url):
    """Fetches a URL and returns text and status code."""
    try:
        headers = {
            "User-Agent": USER_AGENT
        }
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text, response.status_code
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None, None

def crawl_website(url):
    """Crawls a single website for homepage, case studies, and internal pages."""
    domain = get_domain_name(url)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    
    logger.info(f"Starting crawl for {domain}")
    
    # 1. Fetch Homepage
    home_html, status = fetch_url(url)
    if not home_html:
        return
    
    save_raw_html(home_html, domain, "homepage", timestamp)
    
    soup = BeautifulSoup(home_html, 'html.parser')
    
    # 2. Find Case Studies / Success Stories
    # Heuristic: Look for links with "case study", "customer", "success stor" in text or href
    case_study_url = None
    for a in soup.find_all('a', href=True):
        text = a.get_text().lower()
        href = a['href'].lower()
        if "case stud" in text or "success stor" in text or "customers" in text:
            # simple filter to avoid unrelated links
            if "case-studies" in href or "customers" in href:
                case_study_url = urljoin(url, a['href'])
                break
    
    if case_study_url:
        logger.info(f"Found case study link: {case_study_url}")
        cs_html, _ = fetch_url(case_study_url)
        if cs_html:
            save_raw_html(cs_html, domain, "case_study", timestamp)
    
    # 3. Fetch a few internal pages (random 2 links that are internal)
    internal_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(url, href)
        if get_domain_name(full_url) == domain and full_url != url and full_url != case_study_url:
            internal_links.add(full_url)
            if len(internal_links) >= 2:
                break
    
    for i, link in enumerate(internal_links):
        page_html, _ = fetch_url(link)
        if page_html:
            save_raw_html(page_html, domain, f"internal_{i+1}", timestamp)

def run_crawler():
    """Main entry point for crawler."""
    for site in TARGET_WEBSITES:
        crawl_website(site)

if __name__ == "__main__":
    run_crawler()
