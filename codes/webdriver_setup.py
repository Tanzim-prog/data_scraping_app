from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_webdriver(headless=False, wait_time=10):
    # Chrome options to run headless or with specific settings
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new") # Updated headless mode
        chrome_options.add_argument("--disable-gpu") # Prevents WebGL errors
        chrome_options.add_argument("--disable-software-rasterizer")  # Disables WebGL software rendering
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--use-gl=swiftshader")  # Enable software rendering

    # Set a user-agent to prevent bot detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    # Automatically manage ChromeDriver installation
    service = Service(ChromeDriverManager().install())
    
    # Create a new Chrome WebDriver instance with specified options and service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set an implicit wait time (seconds) for element loading
    driver.implicitly_wait(wait_time)
    
    return driver