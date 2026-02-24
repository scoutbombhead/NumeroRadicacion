# NumeroRadicacion Project Structure

## Overview
The NumeroRadicacion project has been refactored into a modular architecture for better maintainability and readability.

## Directory Structure

```
NumeroRadicacion/
├── main.py                      # Main execution script (entry point)
├── config.py                    # Configuration, paths, and logging setup
├── excel_operations.py          # Excel file read/write operations
├── web_driver.py               # Web driver initialization
├── web_scraper.py              # Web scraping and data extraction
├── logs/                        # Log files (auto-created)
├── LOGGING.md                  # Logging documentation
├── README.md                   # This file
├── NumeroRadicacion.xlsx       # Input Excel file
└── NumeroRadicacion - Copy.xlsx
```

## Module Descriptions

### **main.py** (Entry Point)
- Contains only the main execution logic
- Imports functions from other modules
- Clean and easy to follow execution flow
- Run with: `python main.py`

**Key function:**
- `main()` - Orchestrates the entire workflow

### **config.py** (Configuration)
- Global configuration constants (URLs, file paths)
- Logging setup and initialization
- Centralizes all configuration in one place

**Key exports:**
- `logger` - Global logger instance
- `URL` - Target URL
- `EXCEL_FILE_PATH` - Path to Excel file
- `LOG_FILE_PATH` - Path to current log file
- `setup_logging()` - Logger initialization function

### **excel_operations.py** (Excel I/O)
- Read numbers from Excel file
- Write data to Excel spreadsheet
- Handles all spreadsheet operations

**Key functions:**
- `read_numbers_from_excel()` - Reads numbers from column D
- `write_data_to_excel()` - Writes Actuaciones data (columns E-J)
- `write_despacho_to_excel()` - Writes Despacho value (column C)
- `write_sujetos_to_excel()` - Writes Demandante/Demandado (columns A-B)

### **web_driver.py** (Browser Control)
- Web driver initialization
- URL access and page loading

**Key functions:**
- `access_url()` - Opens browser and accesses target URL

### **web_scraper.py** (Web Scraping)
- All web interaction and data extraction
- Button clicking, form filling, data extraction

**Key sections:**

#### Web Interaction:
- `select_second_radio_button()` - Selects radio button
- `enter_search_number()` - Enters search number in form
- `click_consultar_button()` - Clicks search button
- `click_volver_button()` - Clicks return button
- `click_first_clickable_table_number()` - Clicks table number

#### Tab Navigation:
- `click_actuaciones_tab()` - Opens Actuaciones tab
- `click_subjetos_procesales_tab()` - Opens Sujetos Procesales tab

#### Data Extraction:
- `extract_despacho_value()` - Extracts Despacho data
- `print_actuaciones_first_row()` - Extracts Actuaciones row
- `extract_subjetos_procesales()` - Extracts Demandante/Demandado

#### Utilities:
- `wait_for_actuaciones_table_ready()` - Waits for table to load
- `print_datos_proceso_table_debug()` - Debug helper

## How to Use

### Prepare Excel file
Use the excel file in the repository and add all the Radicos to be processed to the D column of the file

### Run the Script
```cmd
python main.py
```

### Check Logs
Logs are saved to: `logs/execution_YYYYMMDD_HHMMSS.log`

For detailed logging information, see `LOGGING.md`

## Dependencies

Required packages:
- selenium
- openpyxl

Install with:
```cmd
pip install selenium openpyxl
```

## Execution Flow

1. **Read Excel** → Get numbers from column D
2. **For each number:**
   - Access the website
   - Select search option (2nd radio button)
   - Enter search number
   - Click search button
   - Click result number
   - **Extract Despacho** → Write to column C
   - **Extract Actuaciones** → Write to columns E-J
   - **Extract Demandante/Demandado** → Write to columns A-B
3. **Save results** → Excel file updated automatically
4. **Log completion** → Check logs for details

## Modular Benefits

✅ **Readability** - Each module has a single responsibility
✅ **Maintainability** - Easy to find and modify specific functionality
✅ **Reusability** - Functions can be imported and used independently
✅ **Testability** - Easier to test individual modules
✅ **Scalability** - Easy to add new features or modules

## Example: Adding New Functionality

To add a new extraction function:

1. Add function to `web_scraper.py`
2. Import in `main.py`
3. Call in the main loop

```python
# In web_scraper.py
def extract_new_data(driver):
    # ... extraction logic ...
    return new_data

# In main.py
from web_scraper import extract_new_data
# Then use it:
new_data = extract_new_data(driver)
```

## Troubleshooting

### Issue: Module not found
- Ensure all Python files are in the same directory
- Check that imports match file names exactly

### Issue: Excel file not found
- Verify path in `config.py`
- Check file exists and is accessible

### Issue: Browser not opening
- Install ChromeDriver compatible with your Chrome version
- Add to PATH or specify path in `web_driver.py`

For logging issues, see `LOGGING.md`

## Contact & Support

For issues or questions, check the logs first:
```cmd
cd logs
type execution_*.log
```

Logs contain detailed execution trace and error messages.
