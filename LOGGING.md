# Logging System Documentation

## Overview
The `NumeroRadicacion` project now uses Python's built-in `logging` module to track execution, errors, and debug information. All logs are automatically saved to files for later analysis.

## Log File Location
- **Directory:** `C:\Users\sauda\PycharmProjects\NumeroRadicacion\logs`
- **File Format:** `execution_YYYYMMDD_HHMMSS.log`
  - Example: `execution_20260224_143022.log`

Each time you run the script, a new timestamped log file is created, making it easy to track multiple executions.

## Log Levels

The logging system uses the following levels:

| Level | Purpose | Example |
|-------|---------|---------|
| **DEBUG** | Detailed information for diagnosing problems | Cell value writes, row processing |
| **INFO** | Confirmation that things are working as expected | Successfully found Demandante, Excel write success |
| **WARNING** | Warning for unexpected situations that may need attention | Despacho not found, missing table data |
| **ERROR** | Error messages for failures that need investigation | Excel file not found, extraction errors |

## Console vs File Output

- **Console (Terminal):** Shows INFO level and above (high-priority messages only)
- **Log File:** Shows DEBUG level and above (all messages including detailed information)

This balance keeps the console clean while preserving all details in the log file.

## Checking Logs When Errors Occur

### If the script completes but something looks wrong:
1. Open the log file from the `logs` folder
2. Search for "ERROR" or "WARNING" to find issues
3. Check the full context around the error

### Example Log Content:
```
2026-02-24 14:30:22 - NumeroRadicacion - INFO - Starting execution - Logs saved to: C:\Users\sauda\PycharmProjects\NumeroRadicacion\logs\execution_20260224_143022.log
2026-02-24 14:30:22 - NumeroRadicacion - INFO - Reading numbers from Excel file: C:\Users\sauda\PycharmProjects\NumeroRadicacion\NumeroRadicacion.xlsx
2026-02-24 14:30:22 - NumeroRadicacion - DEBUG - Row 2: 1001234567890
2026-02-24 14:30:22 - NumeroRadicacion - INFO - Successfully read 5 number(s) from Excel
2026-02-24 14:30:23 - NumeroRadicacion - INFO - Processing number 1/5: 1001234567890
2026-02-24 14:30:23 - NumeroRadicacion - INFO - Attempting to access: https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion
2026-02-24 14:30:25 - NumeroRadicacion - INFO - Successfully accessed URL
2026-02-24 14:30:25 - NumeroRadicacion - INFO - Page title: Consulta de Procesos
```

## Log Levels Used in Code

- **logger.debug()** - Detailed cell writes, row processing, table debugging
- **logger.info()** - Successful operations, data extraction confirmations
- **logger.warning()** - Expected but unexpected situations (missing optional data)
- **logger.error()** - Failures that prevent progress (file not found, extraction failed)

## Tips for Troubleshooting

1. **Start with the log file timestamp** - Find the execution nearest to your run time
2. **Search for "ERROR"** first to see if there were failures
3. **Look at the sequence** - Follow the log chronologically to understand what happened
4. **Check extraction data** - All found Demandante/Demandado values are logged
5. **Excel write confirmations** - Each successful cell write is logged with coordinates

## Clearing Old Logs

If you want to clean up old log files:
```cmd
cd C:\Users\sauda\PycharmProjects\NumeroRadicacion\logs
del *.log
```

Or keep only recent logs manually by deleting older files.

## Log Retention

- Logs are **NOT** automatically deleted
- Keep at least your most recent execution for troubleshooting
- Old logs can be archived or deleted manually as needed
