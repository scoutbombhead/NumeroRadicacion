"""
Web driver initialization and URL access
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time
from config import URL, logger


def access_url(max_retries=2, base_backoff_seconds=5):
    """
    Access the URL and return the driver if successful
    """
    attempt = 0
    while attempt <= max_retries:
        try:
            # Initialize the Chrome driver with basic hardening to reduce bot flags
            chrome_options = Options()
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            driver = webdriver.Chrome(options=chrome_options)

            logger.info(f"Attempting to access: {URL}")
            driver.get(URL)

            # Wait a moment for the page to load
            time.sleep(2)

            if driver.title:
                logger.info("Successfully accessed URL")
                logger.info(f"Page title: {driver.title}")

                # Detect rate limiting / access block responses
                if "403" in driver.title or "Forbidden" in driver.title:
                    logger.warning("Access blocked (403/Forbidden). Backing off before retry.")
                    driver.quit()
                    attempt += 1
                    if attempt > max_retries:
                        logger.error("Failed to access URL after retries (403/Forbidden).")
                        return None

                    # Exponential backoff with light jitter to avoid patterns
                    backoff = (2 ** attempt) * base_backoff_seconds
                    backoff += random.randint(0, 3)
                    logger.info(f"Waiting {backoff} seconds before retry...")
                    time.sleep(backoff)
                    continue

                return driver

            logger.error("Failed to load page (no title found)")
            driver.quit()
            return None

        except Exception as e:
            logger.error(f"Error accessing URL: {str(e)}", exc_info=True)
            return None

    return None