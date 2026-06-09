"""
Web Scraper - Scrapes product/article data from a website and saves to CSV/Excel
Author: Your Name
Description: Extracts titles, prices, links, or any data from websites and exports to file
Usage: python web_scraper.py --url "https://books.toscrape.com" --output results.csv
"""

import requests
import csv
import json
import argparse
import os
from datetime import datetime
from html.parser import HTMLParser


class SimpleHTMLParser(HTMLParser):
    """A lightweight HTML parser to extract tags and data without external libraries."""

    def __init__(self):
        super().__init__()
        self.data_list = []
        self._current_tag = None
        self._current_attrs = {}
        self._capture = False
        self._buffer = ""

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        self._current_attrs = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4", "p", "a", "span", "title"):
            self._capture = True
            self._buffer = ""

    def handle_endtag(self, tag):
        if self._capture and tag == self._current_tag:
            text = self._buffer.strip()
            if text:
                entry = {
                    "tag": tag,
                    "text": text,
                    "href": self._current_attrs.get("href", ""),
                    "class": self._current_attrs.get("class", ""),
                }
                self.data_list.append(entry)
            self._capture = False
            self._buffer = ""

    def handle_data(self, data):
        if self._capture:
            self._buffer += data


def fetch_page(url):
    """Download the HTML content of a page."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None


def scrape(url):
    """Scrape headings, paragraphs, and links from a URL."""
    print(f"\n🌐 Scraping: {url}")
    html = fetch_page(url)
    if not html:
        return []

    parser = SimpleHTMLParser()
    parser.feed(html)

    results = []
    for item in parser.data_list:
        results.append({
            "type": item["tag"].upper(),
            "text": item["text"][:200],  # limit text length
            "link": item["href"] if item["href"] else "N/A",
        })

    print(f"✅ Found {len(results)} items")
    return results


def save_to_csv(data, filename):
    """Save scraped data to a CSV file."""
    if not data:
        print("⚠️ No data to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["type", "text", "link"])
        writer.writeheader()
        writer.writerows(data)
    print(f"💾 Saved to CSV: {filename}")


def save_to_json(data, filename):
    """Save scraped data to a JSON file."""
    if not data:
        print("⚠️ No data to save.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to JSON: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="🌐 Web Scraper - Extract data from any website and save to CSV/JSON"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://books.toscrape.com",
        help="URL to scrape (default: books.toscrape.com demo site)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=f"scraped_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        help="Output filename (.csv or .json)"
    )

    args = parser.parse_args()
    data = scrape(args.url)

    if data:
        if args.output.endswith(".json"):
            save_to_json(data, args.output)
        else:
            save_to_csv(data, args.output)

        print(f"\n📊 Summary: {len(data)} items scraped")
        print("🔍 Preview (first 5 items):")
        for item in data[:5]:
            print(f"  [{item['type']}] {item['text'][:80]}")
    else:
        print("❌ No data scraped.")


if __name__ == "__main__":
    main()
