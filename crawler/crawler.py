from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download_excel(download_path, secret):

    # Retrieve username and password from environment variables
    username = os.environ.get('LIVEIQ_USERNAME')
    password = os.environ.get('LIVEIQ_PASSWORD')

    options = Options() # Configure Chrome options for the webdriver

    # Uncomment the line below to run Chrome in headless mode
    # options.add_argument("--headless")


    # Set preferences for Chrome, including the default download directory
    options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options) # Initialize the Chrome webdriver with the specified options

    # Navigate to the login page
    driver.get("https://liveiq.subway.com/")

    # Wait until the username input field is present, then enter the username
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signInName")))
    driver.find_element(By.ID, "signInName").send_keys(secret['username'])

    # Enter the password in the password input field
    driver.find_element(By.ID, "password").send_keys(secret['password'])

    # Click the login button
    driver.find_element(By.ID, "next").click()

    # Wait until the page loads after login, indicated by the presence of an element with ID 'page-title'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-title")))

    # Navigate to the Employee Export page
    driver.get("https://liveiq.subway.com/Labour/EmployeeExport")

    # Wait for the export button and click
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "exportEmployees")))
    driver.find_element(By.ID, "exportEmployees").click()

    # Handle the popup if it appears
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="noPayrollNumbers"][@class="white-popup mfp-with-anim"]')))
        driver.find_element(By.ID, "validateOkBtn").click()
    except:
        print("No popup appeared.")

    # Wait for the download to complete
    time.sleep(10)  # Adjust this time based on your network speed and file size

    # Close the browser
    driver.quit()

secret = {
    "username": username,
    "password": password
}
download_path = "/path/to/download"
download_excel(download_path, secret)
