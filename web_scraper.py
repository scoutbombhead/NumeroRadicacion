"""
Web scraping functions: clicking buttons, entering data, extracting information
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from config import logger


# ============================================================================
# WEB INTERACTION - Page navigation and form filling
# ============================================================================

def select_second_radio_button(driver):
    """
    Select the 2nd radio button on the page
    """
    try:
        # Wait for radio buttons to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio']"))
        )

        # Find all radio buttons
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")

        if len(radio_buttons) < 2:
            logger.error(f"Found only {len(radio_buttons)} radio button(s), need at least 2")
            return False

        # Use JavaScript to click the 2nd radio button to bypass click interception
        second_radio = radio_buttons[1]
        driver.execute_script("arguments[0].click();", second_radio)
        logger.info(f"Successfully selected 2nd radio button")
        time.sleep(1)
        return True

    except Exception as e:
        logger.error(f"Error selecting radio button: {str(e)}", exc_info=True)
        return False


def enter_search_number(driver, search_number):
    """
    Enter the search number into the text field
    """
    try:
        # Wait for the text input field to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']"))
        )

        # Find the text input field
        text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")

        if len(text_inputs) == 0:
            logger.error(f"No text input field found")
            return False

        # Use the first text input field (most likely the search bar)
        search_field = text_inputs[0]

        # Clear any existing value and enter the search number
        search_field.clear()
        search_field.send_keys(search_number)
        logger.info(f"Successfully entered search number: {search_number}")
        time.sleep(1)
        return True

    except Exception as e:
        logger.error(f"Error entering search number: {str(e)}", exc_info=True)
        return False


def click_consultar_button(driver):
    """
    Click the CONSULTAR button - tries multiple strategies to find it
    """
    try:
        # Strategy 1: Find button by aria-label containing "Consultar"
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Consultar')]"))
            )
            consultar_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Consultar')]")
            driver.execute_script("arguments[0].click();", consultar_button)
            logger.info(f"Successfully clicked CONSULTAR button (Strategy 1 - aria-label)")
            time.sleep(2)
            return True
        except:
            pass

        # Strategy 2: Find button by span text inside button
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(), 'Consultar')]/.."))
            )
            consultar_button = driver.find_element(By.XPATH, "//button//span[contains(text(), 'Consultar')]/..")
            driver.execute_script("arguments[0].click();", consultar_button)
            logger.info(f"Successfully clicked CONSULTAR button (Strategy 2 - span text)")
            time.sleep(2)
            return True
        except:
            pass

        # Strategy 3: Find by button with success class
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'success')]//span[contains(text(), 'Consultar')]"))
            )
            consultar_button = driver.find_element(By.XPATH,
                                                   "//button[contains(@class, 'success')]//span[contains(text(), 'Consultar')]/../..")
            driver.execute_script("arguments[0].click();", consultar_button)
            logger.info(f"Successfully clicked CONSULTAR button (Strategy 3 - success class)")
            time.sleep(2)
            return True
        except:
            pass

        logger.error(f"Could not find CONSULTAR button with any strategy")
        return False

    except Exception as e:
        logger.error(f"Error clicking CONSULTAR button: {str(e)}", exc_info=True)
        return False


def click_volver_button(driver):
    """
    Click the VOLVER button if it appears (in dialog)
    This button may not always appear, so we use a shorter timeout
    """
    try:
        # Strategy 1: Find button by span text "Volver" inside button
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(), 'Volver')]"))
            )
            volver_button = driver.find_element(By.XPATH, "//button//span[contains(text(), 'Volver')]/..")
            driver.execute_script("arguments[0].click();", volver_button)
            logger.info(f"Successfully clicked VOLVER button (Strategy 1 - span text)")
            time.sleep(1)
            return True
        except:
            pass

        # Strategy 2: Find button with aria-label containing "Volver"
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Volver')]"))
            )
            volver_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Volver')]")
            driver.execute_script("arguments[0].click();", volver_button)
            logger.info(f"Successfully clicked VOLVER button (Strategy 2 - aria-label)")
            time.sleep(1)
            return True
        except:
            pass

        # If no VOLVER button is found, it's likely not needed for this search
        logger.info(f"No VOLVER button found (dialog may not have appeared)")
        return True

    except Exception as e:
        logger.error(f"Error clicking VOLVER button: {str(e)}", exc_info=True)
        return False


def click_first_clickable_table_number(driver):
    """
    Find the table and click the first clickable number in the second column
    Starts from the second row (after headers) and checks each row
    """
    try:
        # Wait for the table to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )

        # Find the table
        table = driver.find_element(By.TAG_NAME, "table")

        # Get all rows in the table body
        rows = table.find_elements(By.TAG_NAME, "tr")

        if len(rows) < 2:
            logger.error(f"Table has less than 2 rows (no data rows)")
            return False

        # Iterate through rows starting from the second row (index 1) to skip headers
        for index, row in enumerate(rows[1:], start=2):
            try:
                # Get all cells in this row
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) < 2:
                    logger.debug(f"Row {index} has less than 2 columns, skipping")
                    continue

                # Get the second column (index 1)
                second_column = cells[1]

                # Check if there's a clickable button in the second column
                try:
                    button = second_column.find_element(By.TAG_NAME, "button")
                    # If we found a button, it's clickable
                    number_text = button.text.strip()
                    logger.info(f"Found clickable number in row {index}: {number_text}")

                    # Click the button
                    driver.execute_script("arguments[0].click();", button)
                    logger.info(f"Successfully clicked the number: {number_text}")
                    time.sleep(2)
                    return True

                except:
                    # No button found in this row, check for text
                    try:
                        paragraph = second_column.find_element(By.TAG_NAME, "p")
                        number_text = paragraph.text.strip()
                        logger.debug(f"Row {index} has non-clickable number: {number_text}")
                    except:
                        pass
                    # Continue to the next row
                    continue

            except Exception as e:
                logger.debug(f"Error processing row {index}: {str(e)}")
                continue

        logger.error(f"No clickable numbers found in table")
        return False

    except Exception as e:
        logger.error(f"Error accessing table: {str(e)}", exc_info=True)
        return False


# ============================================================================
# TAB NAVIGATION
# ============================================================================

def click_actuaciones_tab(driver):
    """
    Click the Actuaciones tab
    """
    try:
        # Wait for the tab to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='tab']"))
        )

        # Find the Actuaciones tab by searching for a div with role="tab" containing "Actuaciones"
        actuaciones_tab = driver.find_element(By.XPATH, "//div[@role='tab'][contains(text(), 'Actuaciones')]")

        # Click the tab using JavaScript to avoid any click interception
        driver.execute_script("arguments[0].click();", actuaciones_tab)
        logger.info(f"Successfully clicked Actuaciones tab")
        # Wait a short moment for tab content to load
        time.sleep(1)

        # Wait until an actuaciones table appears to be ready (has a non-timestamp cell)
        if wait_for_actuaciones_table_ready(driver, timeout=8):
            return True
        else:
            # Still return True; logging will help identify issues
            logger.warning("Actuaciones table may not be fully loaded yet")
            return True

    except Exception as e:
        logger.error(f"Error clicking Actuaciones tab: {str(e)}", exc_info=True)
        return False


def click_subjetos_procesales_tab(driver):
    """
    Click the Sujetos Procesales tab
    """
    try:
        # Wait for the tab to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='tab']"))
        )

        # Find the Sujetos Procesales tab by searching for a div with role="tab" containing "Sujetos Procesales"
        tab = driver.find_element(By.XPATH, "//div[@role='tab'][contains(text(), 'Sujetos Procesales')]")

        # Click the tab using JavaScript to avoid any click interception
        driver.execute_script("arguments[0].click();", tab)
        logger.info(f"Successfully clicked Sujetos Procesales tab")
        time.sleep(2)
        return True

    except Exception as e:
        logger.error(f"Error clicking Sujetos Procesales tab: {str(e)}", exc_info=True)
        return False


# ============================================================================
# TABLE EXTRACTION - Extract data from Actuaciones table
# ============================================================================

def wait_for_actuaciones_table_ready(driver, timeout=8):
    """
    Wait until at least one table row contains a non-empty, non-timestamp cell.
    Returns True if ready, False on timeout.
    """
    end_time = time.time() + timeout
    timestamp_re = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}|\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}")
    try:
        while time.time() < end_time:
            tables = driver.find_elements(By.TAG_NAME, "table")
            for t in tables:
                rows = t.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if not cells:
                        cells = row.find_elements(By.TAG_NAME, "th")
                    for cell in cells:
                        try:
                            text = (cell.get_attribute('innerText') or cell.text or "").strip()
                        except:
                            text = (cell.text or "").strip()
                        if not text:
                            continue
                        # if the text doesn't look like a timestamp, consider table ready
                        if not timestamp_re.search(text):
                            return True
            time.sleep(0.5)
        return False
    except Exception:
        return False


def print_actuaciones_first_row(driver):
    """
    Find the Actuaciones table and return the first row.
    Returns the list of cell values for the first row (padded to 6 columns).
    """
    try:
        # Wait for tables to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )

        tables = driver.find_elements(By.TAG_NAME, "table")
        if not tables:
            logger.error("No tables found on Actuaciones tab")
            return []

        # Reuse the same selection heuristics
        chosen_table = None
        best_col_count = 0
        header_keywords = ["fecha", "actuaci", "despacho", "tipo", "documento", "observacion"]
        for t in tables:
            rows = t.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "th")
                if not cells:
                    cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    try:
                        header_text = " ".join(
                            [(cell.get_attribute('innerText') or cell.text).strip().lower() for cell in cells])
                    except Exception:
                        header_text = ""

                    if any(k in header_text for k in header_keywords):
                        chosen_table = t
                        best_col_count = len(cells)
                        break

                    col_count = len(cells)
                    if col_count == 6:
                        chosen_table = t
                        best_col_count = col_count
                        break
                    if col_count > best_col_count:
                        chosen_table = t
                        best_col_count = col_count
                    break
            if best_col_count == 6:
                break

        if chosen_table is None:
            chosen_table = tables[0]

        # Prefer rows in tbody if present (these are typically data rows)
        tbodies = chosen_table.find_elements(By.TAG_NAME, "tbody")
        if tbodies:
            rows = tbodies[0].find_elements(By.TAG_NAME, "tr")
        else:
            rows = chosen_table.find_elements(By.TAG_NAME, "tr")

        if not rows:
            logger.error("Actuaciones table has no rows")
            return []

        # Determine the first data row (row below header):
        if tbodies:
            data_row = rows[0]
        else:
            data_row = rows[1] if len(rows) > 1 else rows[0]
        cells = data_row.find_elements(By.TAG_NAME, "td")
        if not cells:
            cells = data_row.find_elements(By.TAG_NAME, "th")

        row_values = []
        for c in range(6):
            if c < len(cells):
                cell = cells[c]
                try:
                    # prefer common nested elements
                    try:
                        el = cell.find_element(By.TAG_NAME, "button")
                        text = el.get_attribute('innerText') or el.text
                    except:
                        try:
                            el = cell.find_element(By.TAG_NAME, "span")
                            text = el.get_attribute('innerText') or el.text
                        except:
                            try:
                                el = cell.find_element(By.TAG_NAME, "a")
                                text = el.get_attribute('innerText') or el.text
                            except:
                                text = cell.get_attribute('innerText') or cell.text
                except Exception:
                    text = cell.get_attribute('innerText') or cell.text

                if text is None:
                    text = ""
                row_values.append(text.strip())
            else:
                row_values.append("")

        logger.info(f"Actuaciones first row extracted")
        return row_values

    except Exception as e:
        logger.error(f"Error extracting first row of Actuaciones table: {str(e)}", exc_info=True)
        return []


# ============================================================================
# DATOS DE PROCESO - Extract data from Datos de Proceso tab
# ============================================================================

def extract_despacho_value(driver):
    """
    Extract the "Despacho" value from the Datos de Proceso table
    Returns the despacho value as a string, or empty string if not found
    """
    try:
        # Wait for the table to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )

        # Get all tables on the page
        tables = driver.find_elements(By.TAG_NAME, "table")

        if not tables:
            logger.error(f"No tables found in Datos de Proceso")
            return ""

        # Try each table to find the one with Despacho
        for table_idx, table in enumerate(tables):
            rows = table.find_elements(By.TAG_NAME, "tr")

            if not rows:
                continue

            # Look for the row that contains "Despacho:"
            for row in rows:
                try:
                    # Get th and td elements separately (preserve order in DOM)
                    th_elements = row.find_elements(By.TAG_NAME, "th")
                    td_elements = row.find_elements(By.TAG_NAME, "td")

                    if not th_elements or not td_elements:
                        continue

                    # Check if first th is "Despacho:"
                    first_th_text = (th_elements[0].get_attribute('innerText') or th_elements[0].text or "").strip()

                    if first_th_text == "Despacho:" and len(td_elements) > 0:
                        # Get the value from the first td in this row
                        despacho_value = (
                                    td_elements[0].get_attribute('innerText') or td_elements[0].text or "").strip()

                        # Skip if it's a date (YYYY-MM-DD format) or if it looks like a label (contains ":")
                        is_date = len(despacho_value) == 10 and despacho_value[4] == '-' and despacho_value[7] == '-'
                        is_label = ":" in despacho_value and len(despacho_value) < 30

                        if despacho_value and not is_date and not is_label:
                            logger.info(f"Found Despacho: {despacho_value}")
                            return despacho_value
                except:
                    continue

        # If we get here, we didn't find it
        logger.warning(f"Despacho row not found in table")
        print_datos_proceso_table_debug(driver)
        return ""

    except Exception as e:
        logger.error(f"Error extracting Despacho value: {str(e)}", exc_info=True)
        return ""


def print_datos_proceso_table_debug(driver):
    """
    Debug helper: log all table rows to help identify the structure
    """
    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        logger.debug(f"Found {len(tables)} table(s) on Datos de Proceso tab")

        for t_idx, table in enumerate(tables):
            rows = table.find_elements(By.TAG_NAME, "tr")
            logger.debug(f"  Table {t_idx + 1}: {len(rows)} row(s)")

            for r_idx, row in enumerate(rows[:10]):  # Log first 10 rows
                try:
                    # Get all cells
                    cells = row.find_elements(By.TAG_NAME, "th")
                    if not cells:
                        cells = row.find_elements(By.TAG_NAME, "td")

                    row_data = []
                    for cell in cells:
                        text = (cell.get_attribute('innerText') or cell.text or "").strip()
                        row_data.append(
                            text[:50] + ("..." if len(text) > 50 else ""))  # Limit to 50 chars for readability

                    logger.debug(f"    Row {r_idx + 1}: {row_data}")
                except Exception as e:
                    logger.debug(f"    Row {r_idx + 1}: [Error reading row]")
    except Exception as e:
        logger.error(f"Error printing debug info: {str(e)}", exc_info=True)


# ============================================================================
# SUBJETOS PROCESALES - Extract data from Subjetos Procesales tab
# ============================================================================

def extract_subjetos_procesales(driver):
    """
    Extract Demandante and Demandado values from the Subjetos Procesales table
    Returns a dictionary with 'demandante' and 'demandado' keys
    """
    try:
        # Wait for the table to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )

        # Get all tables on the page
        tables = driver.find_elements(By.TAG_NAME, "table")

        if not tables:
            logger.error(f"No tables found in Subjetos Procesales")
            return {"demandante": "", "demandado": ""}

        demandante = ""
        demandado = ""

        # Try each table to find the required data
        for table_idx, table in enumerate(tables):
            rows = table.find_elements(By.TAG_NAME, "tr")

            if not rows:
                continue

            # Look for rows containing "Demandante" and "Demandado"
            for row in rows:
                try:
                    # Get all cells in this row
                    cells = row.find_elements(By.TAG_NAME, "td")

                    if len(cells) >= 2:
                        first_cell_text = (cells[0].get_attribute('innerText') or cells[0].text or "").strip()
                        second_cell_text = (cells[1].get_attribute('innerText') or cells[1].text or "").strip()

                        # Check for Demandante
                        if first_cell_text == "Demandante" and not demandante:
                            demandante = second_cell_text
                            logger.info(f"Found Demandante: {demandante}")

                        # Check for Demandado
                        if first_cell_text == "Demandado" and not demandado:
                            demandado = second_cell_text
                            logger.info(f"Found Demandado: {demandado}")

                        # If we have both, we can stop searching
                        if demandante and demandado:
                            return {"demandante": demandante, "demandado": demandado}

                except:
                    continue

        logger.info(f"Demandante: {demandante if demandante else '(not found)'}")
        logger.info(f"Demandado: {demandado if demandado else '(not found)'}")
        return {"demandante": demandante, "demandado": demandado}

    except Exception as e:
        logger.error(f"Error extracting Subjetos Procesales data: {str(e)}", exc_info=True)
        return {"demandante": "", "demandado": ""}
