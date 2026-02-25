from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

def extract_forms(soup, current_url):
    """
    Extracts structured data from all forms found in the soup object.
    """
    forms = []
    for form_tag in soup.find_all('form'):
        action = form_tag.get('action', '')
        method = form_tag.get('method', 'get').upper()
        
        full_action_url = urljoin(current_url, action) if action else current_url
        
        form_data = {
            'url': current_url,
            'action': full_action_url,
            'method': method,
            'inputs': []
        }
        
        # Look for typical interactive elements inside a form
        for input_tag in form_tag.find_all(['input', 'textarea', 'select', 'button']):
            name = input_tag.get('name')
            if not name:
                continue # Discard unnamed inputs as they are not sent in form submission usually
                
            input_type = input_tag.get('type', 'text') if input_tag.name == 'input' else input_tag.name
            
            form_data['inputs'].append({
                'name': name,
                'type': input_type
            })
            
        forms.append(form_data)
        
    return forms

def crawl(base_url, max_depth=2):
    """
    Crawls internal links starting from base_url up to max_depth.
    Also extracts all HTML forms.
    Returns a tuple of (discovered_urls, discovered_forms).
    """
    visited = set()
    discovered = []
    discovered_forms = []
    
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
            
            # Extract forms
            page_forms = extract_forms(soup, current_url)
            discovered_forms.extend(page_forms)
            
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
            
    return discovered, discovered_forms
