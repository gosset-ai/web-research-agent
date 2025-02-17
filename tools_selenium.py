from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Optional
import os
import atexit

# Global driver instance
_driver = None

def get_driver() -> webdriver.Chrome:
    """Get or create a Selenium WebDriver instance"""
    global _driver
    
    if _driver is not None:
        return _driver
        
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add performance options
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Disable password saving
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
    except ImportError:
        driver_path = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
        
    service = Service(executable_path=driver_path)
    
    _driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    
    # Set custom user agent
    _driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    })
    
    # Register cleanup function
    atexit.register(cleanup_driver)
    
    return _driver

def cleanup_driver():
    """Cleanup function to close the driver when the program exits"""
    global _driver
    if _driver is not None:
        _driver.quit()
        _driver = None

def google_search(query: str) -> List[str]:
    """Search Google and return list of URLs"""
    print(f"\n🔍 Searching Google for: {query}")
    
    driver = get_driver()
    
    try:
        # Navigate to Google search
        search_url = f"https://www.google.com/search?q={query}"
        driver.get(search_url)
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
        )
        
        # Find all result links
        search_results = []
        link_elements = driver.find_elements(By.CSS_SELECTOR, "div.g a")
        
        for element in link_elements:
            url = element.get_attribute("href")
            if url and url.startswith('http') and not url.startswith('https://google.com'):
                search_results.append(url)
        
        return search_results[:10]  # Return top 10 results
        
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_url_content(url: str) -> Optional[str]:
    """Fetch webpage content"""
    print(f"\n📄 Fetching content from: {url}")
    
    driver = get_driver()
    
    try:
        # Set page load timeout
        driver.set_page_load_timeout(10)
        
        # Load the page
        driver.get(url)
        
        # Wait for body to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Remove script and style elements
        driver.execute_script("""
            var elements = document.querySelectorAll('script, style');
            elements.forEach(e => e.remove());
        """)
        
        # Get page content
        text = driver.find_element(By.TAG_NAME, "body").text
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return text if text else None
        
    except Exception as e:
        print(f"Fetch error for {url}: {e}")
        return None 