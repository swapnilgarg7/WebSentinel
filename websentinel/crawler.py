from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

def crawl(base_url, max_depth=2):
    """
    Crawls internal links starting from base_url up to max_depth.
    Returns a list of discovered URLs.
    """
    visited = set()
    discovered = []
    
    # Queue stores tuples of (url, current_depth)
    queue = [(base_url, 0)]
    visited.add(base_url)
    discovered.append(base_url)
    
    base_domain = urlparse(base_url).netloc
    
    while queue:
        current_url, current_depth = queue.pop(0)
        
        if current_depth >= max_depth:
            continue
            
        try:
            response = requests.get(current_url, timeout=5)
            # Only parse HTML content
            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if not href:
                    continue
                    
                full_url = urljoin(current_url, href)
                parsed_url = urlparse(full_url)
                
                # Normalize URL (remove fragments like #section)
                normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                if parsed_url.query:
                    normalized_url += f"?{parsed_url.query}"
                
                if parsed_url.netloc == base_domain:
                    if normalized_url not in visited:
                        visited.add(normalized_url)
                        discovered.append(normalized_url)
                        # Only add to queue if we haven't reached max depth for the next level
                        if current_depth + 1 <= max_depth:
                            queue.append((normalized_url, current_depth + 1))
                        
        except requests.RequestException:
            pass
            
    return discovered
