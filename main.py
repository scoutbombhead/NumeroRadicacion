"""
NumeroRadicacion - Main execution script
Refactored with modular architecture for better maintainability
"""

import time
from config import logger, LOG_FILE_PATH, MAX_RETRIES_PER_NUMBER, RETRY_WAIT_SECONDS
from excel_operations import (
    read_numbers_from_excel,
    write_data_to_excel,
    write_despacho_to_excel,
    write_sujetos_to_excel
)
from web_driver import access_url
from web_scraper import (
    select_second_radio_button,
    enter_search_number,
    click_consultar_button,
    click_volver_button,
    click_first_clickable_table_number,
    click_actuaciones_tab,
    print_actuaciones_first_row,
    extract_despacho_value,
    click_subjetos_procesales_tab,
    extract_subjetos_procesales
)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def process_single_number(driver, number):
    """
    Process a single number through all steps.
    Returns True if successful, False if any critical step fails.
    """
    try:
        # Select the 2nd radio button
        if not select_second_radio_button(driver):
            logger.error(f"Failed to select radio button for {number}")
            return False

        # Enter the search number
        if not enter_search_number(driver, number):
            logger.error(f"Failed to enter search number for {number}")
            return False

        # Click the CONSULTAR button
        if not click_consultar_button(driver):
            logger.error(f"Failed to click CONSULTAR button for {number}")
            return False

        # Click the VOLVER button if a dialog appears
        click_volver_button(driver)

        # Click the first clickable number in the table's second column
        if not click_first_clickable_table_number(driver):
            logger.error(f"Failed to click table number for {number}")
            return False

        # Extract the Despacho value from the Datos de Proceso tab (default view)
        despacho_value = extract_despacho_value(driver)
        if despacho_value:
            logger.info(f"Extracted Despacho value: {despacho_value}")
            # Write Despacho to column C
            write_despacho_to_excel(number, despacho_value)
        else:
            logger.warning(f"Failed to extract Despacho value for {number}")

        # Click the Actuaciones tab
        if not click_actuaciones_tab(driver):
            logger.error(f"Failed to click Actuaciones tab for {number}")
            return False

        # Get the first data row from Actuaciones and write it to Excel (columns E-J)
        first_row = print_actuaciones_first_row(driver)
        if first_row:
            # Ensure exactly 6 columns (E-J)
            row_values = first_row[:6]
            while len(row_values) < 6:
                row_values.append("")

            logger.info(f"Actuaciones first row has {len(row_values)} columns")
            written = write_data_to_excel(number, row_values)
            if written:
                logger.info(f"Wrote Actuaciones first row to Excel for {number}")
            else:
                logger.error(f"Failed to write Actuaciones data to Excel for {number}")
        else:
            logger.info(f"No first row found in Actuaciones table")

        # Write the Despacho value to Excel (column C)
        if despacho_value:
            write_despacho_to_excel(number, despacho_value)

        # Click the Subjetos Procesales tab
        if not click_subjetos_procesales_tab(driver):
            logger.error(f"Failed to click Subjetos Procesales tab for {number}")
            return False

        # Extract Demandante and Demandado values
        sujetos_data = extract_subjetos_procesales(driver)
        if sujetos_data["demandante"] or sujetos_data["demandado"]:
            logger.info(f"Extracted Subjetos Procesales data - Demandante: {sujetos_data['demandante']}, Demandado: {sujetos_data['demandado']}")
            write_sujetos_to_excel(number, sujetos_data["demandante"], sujetos_data["demandado"])
        else:
            logger.warning(f"Failed to extract Subjetos Procesales data for {number}")

        logger.info(f"Successfully completed all steps for: {number}")
        return True

    except Exception as e:
        logger.error(f"Exception during processing {number}: {str(e)}", exc_info=True)
        return False


def main():
    """
    Main execution function with retry mechanism
    """
    logger.info(f"Starting execution - Logs saved to: {LOG_FILE_PATH}")
    
    # Read all numbers from Excel file
    search_numbers = read_numbers_from_excel()

    if not search_numbers:
        logger.warning("No numbers to search. Exiting.")
        return

    # Statistics for reporting
    successful_count = 0
    failed_count = 0

    # Loop through each number
    for index, number in enumerate(search_numbers, start=1):
        logger.info(f"Processing number {index}/{len(search_numbers)}: {number}")

        success = False
        retry_count = 0
        max_attempts = MAX_RETRIES_PER_NUMBER + 1  # Initial attempt + retries

        while retry_count < max_attempts and not success:
            if retry_count > 0:
                logger.info(f"Retry attempt {retry_count}/{MAX_RETRIES_PER_NUMBER} for {number}")
                logger.info(f"Waiting {RETRY_WAIT_SECONDS} seconds before retrying...")
                time.sleep(RETRY_WAIT_SECONDS)

            # Start by accessing the URL
            driver = access_url()

            if driver:
                try:
                    # Process the number through all steps
                    success = process_single_number(driver, number)
                    
                    if not success and retry_count < MAX_RETRIES_PER_NUMBER:
                        logger.warning(f"Processing failed for {number}. Will retry after refreshing...")
                    elif not success:
                        logger.error(f"Processing failed for {number} after {MAX_RETRIES_PER_NUMBER} retries. Moving to next number.")
                        failed_count += 1
                    else:
                        logger.info(f"Successfully processed: {number}")
                        successful_count += 1

                except Exception as e:
                    logger.error(f"Error during search for {number}: {str(e)}", exc_info=True)
                    if retry_count >= MAX_RETRIES_PER_NUMBER:
                        failed_count += 1

                finally:
                    # Close the driver after each attempt
                    driver.quit()
            else:
                logger.error(f"Failed to initialize browser for: {number}")
                if retry_count >= MAX_RETRIES_PER_NUMBER:
                    failed_count += 1

            retry_count += 1

        # Add a delay between searches to avoid rate limiting
        if index < len(search_numbers):
            delay_seconds = 5 + (index % 3)
            logger.info(f"Waiting {delay_seconds} seconds before next search to avoid rate limiting...")
            time.sleep(delay_seconds)

    # Final summary
    logger.info("=" * 60)
    logger.info(f"All {len(search_numbers)} searches completed!")
    logger.info(f"Successful: {successful_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info(f"Success rate: {(successful_count/len(search_numbers)*100):.1f}%")
    logger.info("=" * 60)
    print(f"\n Execution complete! Check logs at: {LOG_FILE_PATH}")
    print(f"  Successful: {successful_count}/{len(search_numbers)}")
    print(f"  Failed: {failed_count}/{len(search_numbers)}")


if __name__ == '__main__':
    main()