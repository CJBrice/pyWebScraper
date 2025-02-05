import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL to monitor
url = "https://www.bhphotovideo.com/c/product/1875466-REG/msi_g5090_32sls_geforce_rtx_5090_suprim.html"

# Function to check stock using Selenium
def check_stock_selenium():
    try:
        print("Initializing WebDriver...")
        options = webdriver.ChromeOptions()
        # Removed headless mode for debugging
        # options.add_argument("--headless")  # Run headless browser (no GURI)
        options.add_argument("--no-sandbox")  # Disable sandboxing

        # Set up Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Set a longer page load timeout to ensure full page loads
        driver.set_page_load_timeout(30)  # Set timeout to 30 seconds

        print(f"Navigating to {url}...")
        driver.get(url)

        # Wait for the page to load (sleep for a few seconds to make sure)
        time.sleep(5)  # Give the page some time to load

        # Wait for the element to be present (timeout after 10 seconds)
        wait = WebDriverWait(driver, 10)
        stock_xpath = '//*[@id="bh-app"]/section/div/div[2]/div[5]/div/div[2]/div/div/div[2]/div[2]/div/div/span'

        print("Waiting for stock element...")
        # Wait for the stock element to appear
        try:
            stock_element = wait.until(EC.presence_of_element_located((By.XPATH, stock_xpath)))
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
