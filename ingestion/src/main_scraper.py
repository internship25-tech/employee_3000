import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from run_scraper import run_scraper

if __name__ == "__main__":
    print("Starting scraper...")
    run_scraper()
    print("Scraper completed.")
