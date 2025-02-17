import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import quote_plus

def google_search(query: str) -> List[str]:
    """Search Google and return list of URLs"""
    print(f"\n🔍 Searching Google for: {query}")
    
    # Add a user agent to avoid blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Encode the search query
    encoded_query = quote_plus(query)
    url = f'https://www.google.com/search?q={encoded_query}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        # Find all result divs
        for result in soup.find_all('div', class_='g'):
            link = result.find('a')
            if link and 'href' in link.attrs:
                url = link['href']
                if url.startswith('http') and not url.startswith('https://google.com'):
                    search_results.append(url)
        
        return search_results[:10]  # Return top 10 results
        
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_url_content(url: str) -> str:
    """Fetch webpage content"""
    print(f"\n📄 Fetching content from: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        print(f"Fetch error for {url}: {e}")
        return None 