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
        print("Crawling for internal links and extracting forms...")
        
        discovered_urls, discovered_forms = crawler.crawl(args.url)
        
        print("\nDiscovered URLs:")
        for url in discovered_urls:
            print(f"  - {url}")
            
        print(f"\nTotal pages discovered: {len(discovered_urls)}")
        
        print(f"\nDiscovered Forms: {len(discovered_forms)}")
        print("=================" + "=" * len(str(len(discovered_forms))))
        for form in discovered_forms:
            print(f"URL: {form['url']}")
            print(f"  Action: {form['action']}")
            print(f"  Method: {form['method']}")
            print("  Inputs:")
            if not form['inputs']:
                print("    (No named inputs found)")
            for form_input in form['inputs']:
                print(f"    - name: {form_input['name']}, type: {form_input['type']}")
            print("")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
