import argparse
import sys

try:
    from websentinel import crawler
except ImportError:
    import crawler

def main():
    parser = argparse.ArgumentParser(description="WebSentinel - Security Testing CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: scan
    scan_parser = subparsers.add_parser("scan", help="Scan a target URL")
    scan_parser.add_argument("url", type=str, help="The target URL to scan")

    args = parser.parse_args()

    if args.command == "scan":
        print(f"Starting scan for: {args.url}")
        print("Crawling for internal links...")
        
        discovered_urls = crawler.crawl(args.url)
        
        print("\nDiscovered URLs:")
        for url in discovered_urls:
            print(f"  - {url}")
            
        print(f"\nTotal pages discovered: {len(discovered_urls)}")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
