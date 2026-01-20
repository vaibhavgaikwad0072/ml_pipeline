import os
import json
import logging
from datetime import datetime
from src.config import PROCESSED_DATA_DIR, METRICS_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_aggregator():
    """Aggregates metrics from processed data."""
    if not os.path.exists(PROCESSED_DATA_DIR):
        logger.warning("No processed data found.")
        return

    all_records = []
    
    # Load all data
    for domain in os.listdir(PROCESSED_DATA_DIR):
        domain_path = os.path.join(PROCESSED_DATA_DIR, domain)
        if not os.path.isdir(domain_path):
            continue
            
        for timestamp in os.listdir(domain_path):
            ts_path = os.path.join(domain_path, timestamp)
            json_path = os.path.join(ts_path, "data.json")
            
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    try:
                        records = json.load(f)
                        all_records.extend(records)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to decode {json_path}")

    if not all_records:
        logger.info("No records to aggregate.")
        return

    # Compute Metrics
    websites = set()
    websites_with_cs = set()
    section_lengths = {}

    for r in all_records:
        website = r.get("website")
        websites.add(website)
        
        section = r.get("section")
        content = r.get("content", "")
        length = len(content)
        
        if section == "case_study" and length > 0:
            websites_with_cs.add(website)
        
        if section not in section_lengths:
            section_lengths[section] = []
        section_lengths[section].append(length)

    stats = {
        "total_websites_crawled": len(websites),
        "websites_with_case_studies": len(websites_with_cs),
        "active_websites": len(websites), # Assuming all crawled are active for now
        "content_length_stats": {}
    }

    for section, lengths in section_lengths.items():
        if lengths:
            stats["content_length_stats"][section] = {
                "count": len(lengths),
                "avg_length": sum(lengths) / len(lengths),
                "min_length": min(lengths),
                "max_length": max(lengths)
            }

    # Save Metrics
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    if not os.path.exists(METRICS_DIR):
        os.makedirs(METRICS_DIR)
        
    save_path = os.path.join(METRICS_DIR, f"aggregation_{timestamp}.json")
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    logger.info(f"Aggregation complete. Saved to {save_path}")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    run_aggregator()
