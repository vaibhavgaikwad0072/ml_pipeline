import os
import json
import logging
from bs4 import BeautifulSoup
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, NAVBAR_TAGS, NAVBAR_CLASSES, FOOTER_TAGS, FOOTER_CLASSES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def extract_section(soup, tags, classes):
    """Helper to find content based on tags and class names."""
    for tag in tags:
        element = soup.find(tag)
        if element:
            return clean_text(element.get_text())
    
    for cls in classes:
        element = soup.find(class_=lambda x: x and cls in x.lower())
        if element:
            return clean_text(element.get_text())
            
        element = soup.find(id=lambda x: x and cls in x.lower())
        if element:
            return clean_text(element.get_text())
            
    return ""

def process_html_file(filepath, domain, timestamp, page_type):
    """Parses HTML and returns structured data records."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    records = []
    
    # Base record structure
    base_record = {
        "website": f"https://{domain}",
        "crawl_timestamp": timestamp,
        "isActive": True # Assuming if we crawled it, it's active
    }

    if page_type == "homepage":
        # Extract Navbar
        navbar_text = extract_section(soup, NAVBAR_TAGS, NAVBAR_CLASSES)
        records.append({**base_record, "section": "navbar", "content": navbar_text})

        # Extract Footer
        footer_text = extract_section(soup, FOOTER_TAGS, FOOTER_CLASSES)
        records.append({**base_record, "section": "footer", "content": footer_text})

        # Extract Homepage Content (Body text)
        body_text = clean_text(soup.body.get_text() if soup.body else "")
        records.append({**base_record, "section": "homepage", "content": body_text[:5000]})

    elif page_type == "case_study":
        content_text = clean_text(soup.body.get_text() if soup.body else "")
        records.append({**base_record, "section": "case_study", "content": content_text[:5000]})

    return records

def run_processor():
    """Main entry point for processor."""
    if not os.path.exists(RAW_DATA_DIR):
        logger.warning("No raw data found.")
        return

    for domain in os.listdir(RAW_DATA_DIR):
        domain_path = os.path.join(RAW_DATA_DIR, domain)
        if not os.path.isdir(domain_path):
            continue
            
        for timestamp in os.listdir(domain_path):
            ts_path = os.path.join(domain_path, timestamp)
            if not os.path.isdir(ts_path):
                continue
            
            all_records = []
            
            # Process Homepage
            hp_path = os.path.join(ts_path, "homepage.html")
            all_records.extend(process_html_file(hp_path, domain, timestamp, "homepage"))
            
            # Process Case Study
            cs_path = os.path.join(ts_path, "case_study.html")
            all_records.extend(process_html_file(cs_path, domain, timestamp, "case_study"))

            # Save Processed Data
            if all_records:
                save_dir = os.path.join(PROCESSED_DATA_DIR, domain, timestamp)
                os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, "data.json")
                
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(all_records, f, indent=2)
                
                logger.info(f"Processed data for {domain} at {timestamp} saved to {save_path}")

if __name__ == "__main__":
    run_processor()
