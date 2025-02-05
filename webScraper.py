import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Retrieve GitHub token from environment variable (optional for GitHub API access)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Ensure the environment variable is set

if not GITHUB_TOKEN:
    print("GitHub token not set, but this is fine for local usage.")  # No exception here if you're not using it for now

# Path to your local geckodriver
geckodriver_path = r"C:\geckodriver\geckodriver.exe"  # Update this to your local path

# Path to your Firefox binary (update this if Firefox is installed in a custom location)
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Default install path for Firefox

if not os.path.exists(geckodriver_path):
    raise Exception(f"Geckodriver not found at {geckodriver_path}. Please download and place it in this location.")

if not os.path.exists(firefox_binary_path):
    raise Exception(f"Firefox not found at {firefox_binary_path}. Please ensure Firefox is installed and update the path.")

# URL to monitor
url = "https://www.bhphotovideo.com/c/product/1875466-REG/msi_g5090_32sls_geforce_rtx_5090_suprim.html"

# Function to check stock using Selenium
def check_stock_selenium():
    try:
        print("Initializing WebDriver...")
        options = Options()
        options.add_argument("--headless")  # Run headless browser (no GUI)
        options.add_argument("--disable-gpu")  # Disable GPU acceleration (important for headless)
        options.add_argument("--no-sandbox")  # Disable sandboxing for headless mode
        options.binary_location = firefox_binary_path  # Set the Firefox binary location

        # Set up Firefox WebDriver using local Geckodriver
        service = FirefoxService(executable_path=geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)

        # Set a longer page load timeout to ensure full page loads
        driver.set_page_load_timeout(40)  # Set timeout to 40 seconds

        print(f"Navigating to {url}...")
        driver.get(url)

        # Wait for the page to load (use explicit wait)
        wait = WebDriverWait(driver, 30)  # Increase wait time

        stock_xpath = '//*[@id="bh-app"]/section/div/div[2]/div[5]/div/div[2]/div/div/div[2]/div[2]/div/div/span'

        print("Waiting for stock element...")
        try:
            # Wait for the stock element to appear with explicit wait
            stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, stock_xpath)))
            print("Stock element found, checking status...")
            stock_text = stock_element.text.strip()

            if "In Stock" in stock_text:
                print("Back in stock! 🚀")
            else:
                print("Still out of stock 😞")
        except Exception as e:
            print(f"Error finding stock status: {e}")

        driver.quit()

    except Exception as e:
        print(f"An error occurred with Selenium: {e}")

# Infinite loop to check every 10 seconds
while True:
    check_stock_selenium()
    print("Waiting 10 seconds before next check...\n")
    time.sleep(10)  # Wait for 10 seconds before checking again
