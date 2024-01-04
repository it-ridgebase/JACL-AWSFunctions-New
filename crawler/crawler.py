from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob
import logging
import tempfile
from dotenv import load_dotenv

def get_latest_file(download_path, file_extension):
    # List all files with the given extension
    list_of_files = glob.glob(os.path.join(download_path, f"*.{file_extension}")) 
    if not list_of_files:  # No files found
        return None
    # Get the latest file
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def download_excel(download_path, secret):
    logger = logging.getLogger(__name__)
    logger.debug("Starting the download process.")
    downloaded_file_path = None

    options = Options()  # Configure Chrome options for the webdriver
    # Uncomment the line below to run Chrome in headless mode
    # options.add_argument("--headless")

    # Set preferences for Chrome, including the default download directory
    options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    logger.debug("WebDriver initialized.")
    driver = webdriver.Chrome(options=options)  # Initialize the Chrome webdriver with the specified options
    try:
        # Navigate to the login page
        driver.get("https://liveiq.subway.com/")
        logger.debug("Navigated to the login page.")

        # Wait until the username input field is present, then enter the username
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signInName")))
        driver.find_element(By.ID, "signInName").send_keys(secret['username'])

        # Enter the password in the password input field
        driver.find_element(By.ID, "password").send_keys(secret['password'])

        # Click the login button
        driver.find_element(By.ID, "next").click()

        # Wait until the page loads after login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-title")))
        logger.debug("Logged in successfully. Navigating to the download page.")

        # Navigate to the Employee Export page and perform necessary actions
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
        logger.debug("Waiting for the file to download.")
        time.sleep(10)  # Adjust this time based on your network speed and file size

        downloaded_file_path = get_latest_file(download_path, "xlsx")

        if downloaded_file_path:
            logger.debug(f"Downloaded file found: {downloaded_file_path}")
        else:
            logger.warning("No file was downloaded.")

    except Exception as e:
        logger.exception("An error occurred during the download process.")

    finally:
    # Close the browser
        driver.quit()
        logger.debug("WebDriver closed.")

    return downloaded_file_path

def main():
    load_dotenv()  # Load environment variables from .env file

    username = os.environ.get('LIVEIQ_USERNAME')
    password = os.environ.get('LIVEIQ_PASSWORD')
    secret = {
        "username": username,
        "password": password
    }
    download_path = tempfile.mkdtemp()
    downloaded_file = download_excel(download_path, secret)
    if downloaded_file:
        print(f"Downloaded file: {downloaded_file}")
    else:
        print("No file was downloaded.")

if __name__ == "__main__":
    main()
