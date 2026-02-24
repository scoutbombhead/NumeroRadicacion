"""
Web driver initialization and URL access
"""

from selenium import webdriver
import time
from config import URL, logger


def access_url():
    """
    Access the URL and return the driver if successful
    """
    try:
        # Initialize the Chrome driver
        driver = webdriver.Chrome()

        logger.info(f"Attempting to access: {URL}")
        driver.get(URL)

        # Wait a moment for the page to load
        time.sleep(2)

        # Check if page loaded successfully
        if driver.title:
            logger.info(f"Successfully accessed URL")
            logger.info(f"Page title: {driver.title}")
            return driver
        else:
            logger.error("Failed to load page (no title found)")
            driver.quit()
            return None

    except Exception as e:
        logger.error(f"Error accessing URL: {str(e)}", exc_info=True)
        return None
