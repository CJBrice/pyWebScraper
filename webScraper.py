import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

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

        # Set up Firefox WebDriver
        service = FirefoxService(GeckoDriverManager().install())
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

# Infinite loop to check every 15 seconds
while True:
    check_stock_selenium()
    print("Waiting 15 seconds before next check...\n")
    time.sleep(15)  # Wait for 15 seconds before checking again
