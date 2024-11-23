import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options to make the browser appear less automated
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--incognito")  # Optional: Use incognito mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

# Set up the Chrome driver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Remove Selenium-specific flags to avoid detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    });
    """
})

try:
    # Open the Kalshi Crypto Events page
    url = "https://kalshi.com/events/crypto"
    driver.get(url)

    # Wait for the page to load fully
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span"))
    )

    # Find all span elements (you may need to refine this selector for specific spans)
    spans = driver.find_elements(By.XPATH, "//span")

    for i, span in enumerate(spans, start=1):
        try:
            # Click on the span
            print(f"Clicking on Span {i}: {span.text}")
            span.click()

            # Wait for the next page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div[6]/div/div/div/div[1]/div[1]/div/section/span")
                )
            )

            # Check if the target element exists
            try:
                target_element = driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div/div[6]/div/div/div/div[1]/div[1]/div/section/span/div/div[2]/div[2]/div[3]/div[4]/div/div/div",
                )
                print(f"Target element found on Span {i} page.")
            except Exception:
                print(f"Target element not found on Span {i} page. Skipping...")
                driver.back()  # Go back to the previous page
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span"))
                )
                continue

            # Extract and print values from the specified sequence of XPaths
            value_xpaths = [
                "/html/body/div[1]/div/div[6]/div/div/div/div[1]/div[1]/div/section/span/div/div[2]/div[2]/div[3]/div[1]/div/div[1]",
                "/html/body/div[1]/div/div[6]/div/div/div/div[1]/div[1]/div/section/span/div/div[2]/div[2]/div[3]/div[2]/div/div/div[4]/span/div/div/span",
            ]

            for xpath in value_xpaths:
                try:
                    value = driver.find_element(By.XPATH, xpath).text
                    print(f"Value from {xpath}: {value}")
                except Exception:
                    print(f"Value not found for XPath: {xpath}")

            # Navigate back to the previous page
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span"))
            )

        except Exception as e:
            print(f"An error occurred while processing Span {i}: {e}")

finally:
    # Close the browser after completion
    print("Closing the browser...")
    driver.quit()
