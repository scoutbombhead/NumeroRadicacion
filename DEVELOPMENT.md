# Development Guide

## Quick Reference

### File Responsibilities

| File | Responsibility | Lines |
|------|---|---|
| `main.py` | Orchestrate workflow | ~110 |
| `config.py` | Configuration & logging | ~60 |
| `excel_operations.py` | Excel read/write | ~150 |
| `web_driver.py` | Browser setup | ~35 |
| `web_scraper.py` | Web interaction & extraction | ~650 |

### Import Structure

```
main.py
├── config.py (logger, paths)
├── excel_operations.py (Excel functions)
├── web_driver.py (Browser access)
└── web_scraper.py (Web interaction)
```

## Adding New Features

### Example 1: Add a New Data Extraction

**Step 1:** Create extraction function in `web_scraper.py`
```python
def extract_custom_data(driver):
    """Extract custom data from page"""
    try:
        # ... extraction logic ...
        logger.info(f"Found custom data: {data}")
        return data
    except Exception as e:
        logger.error(f"Error extracting custom data: {str(e)}", exc_info=True)
        return ""
```

**Step 2:** Add write function to `excel_operations.py`
```python
def write_custom_data_to_excel(search_number, custom_data):
    """Write custom data to column X"""
    try:
        workbook = load_workbook(EXCEL_FILE_PATH)
        worksheet = workbook.active
        
        # Find row with search_number in column D
        # Write to desired column
        # Save workbook
        logger.info(f"Wrote custom data to Excel for: {search_number}")
        return True
    except Exception as e:
        logger.error(f"Error writing custom data: {str(e)}", exc_info=True)
        return False
```

**Step 3:** Call in `main.py`
```python
from web_scraper import extract_custom_data
from excel_operations import write_custom_data_to_excel

# In main loop:
custom_data = extract_custom_data(driver)
write_custom_data_to_excel(number, custom_data)
```

### Example 2: Add a New Tab Navigation

**Step 1:** Create tab clicking function in `web_scraper.py`
```python
def click_new_tab(driver):
    """Click the New Tab"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='tab']"))
        )
        tab = driver.find_element(By.XPATH, "//div[@role='tab'][contains(text(), 'New Tab')]")
        driver.execute_script("arguments[0].click();", tab)
        logger.info(f"Successfully clicked New Tab")
        time.sleep(2)
        return True
    except Exception as e:
        logger.error(f"Error clicking New Tab: {str(e)}", exc_info=True)
        return False
```

**Step 2:** Call in `main.py` execution loop

## Logging Best Practices

### Use Appropriate Levels

```python
# DEBUG - For detailed diagnostic info
logger.debug(f"Processing row {index}")

# INFO - For successful operations
logger.info(f"Successfully found: {data}")

# WARNING - For unexpected but recoverable situations
logger.warning(f"Data not found, continuing anyway")

# ERROR - For failures needing investigation
logger.error(f"Failed to extract data: {error}", exc_info=True)
```

### Always Log Exceptions

```python
# BAD
except Exception as e:
    print(f"Error: {e}")

# GOOD
except Exception as e:
    logger.error(f"Detailed context: {str(e)}", exc_info=True)
```

## Code Style Guidelines

### Function Documentation
```python
def my_function(param1, param2):
    """
    Brief description of what function does
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
```

### Error Handling
```python
try:
    # ... code ...
except SpecificException as e:
    logger.error(f"Specific context: {str(e)}", exc_info=True)
    return False
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return False
```

### Variable Naming
- Use descriptive names: `despacho_value` not `dv`
- Use snake_case for variables: `search_number` not `searchNumber`
- Use UPPER_CASE for constants: `EXCEL_FILE_PATH`

## Testing Individual Modules

### Test Excel Operations
```python
# test_excel.py
from excel_operations import read_numbers_from_excel

numbers = read_numbers_from_excel()
print(f"Found {len(numbers)} numbers")
```

### Test Web Scraping
```python
# test_web.py
from web_driver import access_url
from web_scraper import select_second_radio_button

driver = access_url()
if driver:
    select_second_radio_button(driver)
    driver.quit()
```

## Performance Tips

1. **Batch Excel Writes** - Consider batching multiple writes
2. **Wait Times** - Keep `time.sleep()` calls minimal
3. **Browser Memory** - Always close driver in finally block
4. **Logging** - Excessive DEBUG logging can slow execution

## Debugging Tips

### Check Logs First
```cmd
cd logs
type execution_20260224_143022.log
```

### Add Temporary Debug Logging
```python
logger.debug(f"Variable state: {variable}")
```

### Use Browser Inspector
- Right-click element in Chrome
- Select "Inspect" to find correct XPath

### Test XPath in Console
```javascript
// In browser console
document.evaluate("//button[contains(text(), 'Search')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
```

## Refactoring Checklist

When adding new code:
- ✅ Add docstrings to functions
- ✅ Use appropriate logging levels
- ✅ Handle exceptions with `exc_info=True`
- ✅ Update relevant module only (separation of concerns)
- ✅ Add imports to `main.py`
- ✅ Test in isolation first
- ✅ Check logs for unexpected behavior

## Common Patterns

### Pattern 1: Excel Row Lookup
```python
target_row = None
for row_index, row in enumerate(worksheet.iter_rows(min_row=2, min_col=4, max_col=4), start=2):
    cell_val = row[0].value
    if cell_val is not None and str(cell_val).strip() == str(search_number).strip():
        target_row = row_index
        break

if target_row is None:
    logger.error(f"Number {search_number} not found")
    return False
```

### Pattern 2: Multi-Strategy Element Finding
```python
try:
    # Strategy 1
    element = driver.find_element(By.XPATH, "//button[@id='btnSearch']")
    logger.info("Found via Strategy 1")
    return element
except:
    pass

try:
    # Strategy 2
    element = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    logger.info("Found via Strategy 2")
    return element
except:
    pass

logger.error("Element not found with any strategy")
return None
```

### Pattern 3: Safe Text Extraction
```python
try:
    text = (element.get_attribute('innerText') or element.text or "").strip()
except Exception:
    text = (element.text or "").strip()
```

## Version History

- **v1.0** - Initial refactor into modular architecture
  - Split main.py into 5 focused modules
  - Improved logging system
  - Added comprehensive documentation

## Future Improvements

- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Create CLI argument parser for custom runs
- [ ] Add progress bar for batch operations
- [ ] Create admin dashboard for monitoring
- [ ] Add data validation layer
- [ ] Implement retry logic for failed extractions
