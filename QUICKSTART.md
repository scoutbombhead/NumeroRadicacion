# Quick Start Guide

## Installation

### 1. Install Python Dependencies
```cmd
pip install selenium openpyxl
```

### 2. Download ChromeDriver
- Download from: https://chromedriver.chromium.org/
- Extract and add to PATH, or place in project directory

### 3. Verify Setup
```cmd
python -c "from selenium import webdriver; print('Selenium OK')"
python -c "from openpyxl import load_workbook; print('OpenPyXL OK')"
```

## Running the Script

### Simple Run
```cmd
python main.py
```

The script will:
1. Read numbers from `NumeroRadicacion.xlsx` column D
2. Search each number on the website
3. Extract and write data automatically
4. Save results to Excel file

### Check Results

**In Excel:**
- Column A: Demandante
- Column B: Demandado
- Column C: Despacho
- Columns E-J: Actuaciones data

**In Logs:**
```cmd
cd logs
dir  # See all log files
type execution_*.log  # Read latest log
```

## File Structure

```
Project/
├── main.py              ← Run this file
├── config.py            ← Configuration
├── excel_operations.py  ← Excel read/write
├── web_driver.py        ← Browser control
├── web_scraper.py       ← Web interaction
├── NumeroRadicacion.xlsx ← Your data
└── logs/                ← Log files
```

## Troubleshooting

### Problem: Browser won't open
**Solution:** 
- Install ChromeDriver matching your Chrome version
- Add to PATH or check `web_driver.py` for path

### Problem: Excel file not found
**Solution:**
- Ensure `NumeroRadicacion.xlsx` is in project folder
- Check path in `config.py`

### Problem: No data extracted
**Solution:**
- Check logs: `cd logs && type execution_*.log`
- Look for ERROR messages
- Website structure may have changed

### Problem: Slow execution
**Solution:**
- Normal - web scraping takes time
- Each search takes 10-15 seconds
- Check logs for delays

## Configuration

### Change Input Excel File
Edit `config.py`:
```python
EXCEL_FILE_PATH = os.path.join(BASE_DIR, "your_file.xlsx")
```

### Change Search URL
Edit `config.py`:
```python
URL = "https://your-url.com"
```

### Enable More Detailed Logging
In `config.py`, change console handler level:
```python
console_handler.setLevel(logging.DEBUG)  # Instead of INFO
```

## Tips & Tricks

### Tip 1: Test One Number First
Modify Excel to have just one number, run script to test:
```cmd
python main.py
```

### Tip 2: Check Log While Running
In another terminal:
```cmd
cd logs
type execution_*.log | more
```

### Tip 3: Prepare Excel Data
Before running:
- Column D must have case numbers
- No empty rows in between
- Close Excel before running (avoids conflicts)

### Tip 4: Monitor Progress
Watch log file updates:
```cmd
cd logs
tail -f execution_*.log  # On Unix/Git Bash
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| No numbers found | Column D empty or wrong file | Check Excel file has data in D |
| Browser doesn't open | ChromeDriver missing | Install ChromeDriver |
| Excel not updated | Script crashed | Check logs for errors |
| Slow execution | Normal | Each search takes ~10-15s |
| Module not found | Missing dependencies | Run `pip install -r requirements.txt` |

## What Gets Extracted

### From Despacho Tab
- **Column C:** Court/Despacho name

### From Actuaciones Tab
- **Columns E-J:** First action row data
  - E: Date
  - F: Acción (Action)
  - G: Despacho
  - H: Type
  - I: Document
  - J: Observation

### From Sujetos Procesales Tab
- **Column A:** Demandante (Plaintiff)
- **Column B:** Demandado (Defendant)

## Running Multiple Batches

### Safe Way
1. Complete first batch
2. Create new Excel file with next numbers
3. Update `config.py` with new file path
4. Run script again

### Or
1. Add more numbers to column D
2. Run script again - it will process all
3. Previously extracted data remains unchanged

## Advanced: Command Line Arguments

To add custom arguments in future:

```python
# In main.py
import sys

if len(sys.argv) > 1:
    excel_file = sys.argv[1]
else:
    excel_file = EXCEL_FILE_PATH
```

Then run:
```cmd
python main.py custom_file.xlsx
```

## Performance Expectations

- Reading Excel: < 1 second
- Per search: 10-15 seconds (depends on internet)
- Data extraction: 1-2 seconds
- Excel writing: < 1 second
- Typical batch of 10: ~2-3 minutes

## Safety Features

✅ **Automatic Logging** - All actions logged
✅ **Error Recovery** - Continues on single failures
✅ **Excel Safety** - Uses openpyxl for safe writes
✅ **Driver Cleanup** - Always closes browser

## After Execution

1. **Review Results**
   - Open `NumeroRadicacion.xlsx`
   - Check columns A, B, C, E-J are filled

2. **Check Logs**
   - Look at `logs/execution_*.log`
   - Search for "ERROR" if issues

3. **Export Results**
   - Save Excel to desired location
   - Create backup if needed

## Next Steps

- See `README.md` for detailed architecture
- See `DEVELOPMENT.md` for advanced usage
- See `LOGGING.md` for detailed logging info

## Support

Check these in order:
1. Logs folder - See detailed execution trace
2. README.md - Architecture and structure
3. DEVELOPMENT.md - Advanced configuration
4. LOGGING.md - Troubleshooting logs

**Most issues are visible in the logs!** 📋
