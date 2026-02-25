# Project Structure Overview

## Directory Tree

```
NumeroRadicacion/
│
├── 📄 MAIN EXECUTION
│   └── main.py (110 lines)
│       Entry point - Orchestrates entire workflow
│
├── 🔧 CORE MODULES
│   ├── config.py (60 lines)
│   │   Configuration, paths, and logging setup
│   │
│   ├── excel_operations.py (150 lines)
│   │   Read from and write to Excel files
│   │
│   ├── web_driver.py (35 lines)
│   │   Browser initialization and URL access
│   │
│   └── web_scraper.py (650 lines)
│       Web interaction, clicking, and data extraction
│
├── 📚 DOCUMENTATION
│   ├── README.md
│   │   Complete architecture and module descriptions
│   │
│   ├── QUICKSTART.md
│   │   Get started in 5 minutes
│   │
│   ├── DEVELOPMENT.md
│   │   Add features and best practices
│   │
│   ├── LOGGING.md
│   │   Logging system and troubleshooting
│   │
│   └── REFACTORING_SUMMARY.md
│       What changed in this refactoring
│
├── 📊 DATA
│   ├── NumeroRadicacion.xlsx
│   │   Main input/output file (columns A-J)
│   │
│   └── NumeroRadicacion - Copy.xlsx
│       Backup copy
│
├── 📝 LOGS (auto-created)
│   └── execution_YYYYMMDD_HHMMSS.log
│       Execution logs for debugging
│
└── 🔐 SYSTEM FILES
    ├── .git/
    ├── .idea/
    └── .venv/
        Virtual environment
```

## Module Diagram

```
╔══════════════════════════════════════════════════════════════════╗
║                          main.py                                 ║
║                    (Clean Entry Point)                           ║
║                        110 lines                                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Imports:                                                        ║
║  ├─ From config: logger, LOG_FILE_PATH                          ║
║  ├─ From excel_operations: read, write functions                ║
║  ├─ From web_driver: access_url                                 ║
║  └─ From web_scraper: click, extract functions                  ║
║                                                                  ║
║  Main Loop:                                                      ║
║  1. Read numbers from Excel                                      ║
║  2. For each number:                                             ║
║     a. Access URL                                                ║
║     b. Fill form & search                                        ║
║     c. Extract data (Despacho, Actuaciones, Sujetos)             ║
║     d. Write to Excel                                            ║
║  3. Log completion                                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

          ▲                  ▲                   ▲
          │                  │                   │
    ┌─────┴────────┐   ┌────┴────────┐   ┌─────┴──────────┐
    │              │   │             │   │                │
    ▼              ▼   ▼             ▼   ▼                ▼

┌─────────────┐ ┌──────────────────┐ ┌────────────┐ ┌───────────────────┐
│  config.py  │ │ excel_operations │ │ web_driver │ │  web_scraper.py   │
│  (60 lines) │ │   (150 lines)    │ │ (35 lines) │ │   (650 lines)     │
├─────────────┤ ├──────────────────┤ ├────────────┤ ├───────────────────┤
│ • Logger    │ │ • read_numbers   │ │ • access   │ │ • select_button   │
│ • URLs      │ │ • write_data     │ │   _url     │ │ • enter_number    │
│ • Paths     │ │ • write_despacho │ │            │ │ • click_button    │
│ • Logging   │ │ • write_sujetos  │ │            │ │ • click_tab       │
│   setup     │ │                  │ │            │ │ • extract_data    │
└─────────────┘ └──────────────────┘ └────────────┘ └───────────────────┘
```

## Data Flow

```
START
  │
  ├─► config.py: Setup logging
  │
  ├─► excel_operations.read_numbers_from_excel()
  │   └─► Get list: [123456, 234567, 345678, ...]
  │
  ├─► FOR EACH NUMBER:
  │   │
  │   ├─► web_driver.access_url()
  │   │   └─► Browser opens
  │   │
  │   ├─► web_scraper: Click, enter, search
  │   │   └─► Browser navigates & fills form
  │   │
  │   ├─► web_scraper: Extract Despacho
  │   │   └─► "Juzgado Civil No. 5"
  │   │
  │   ├─► web_scraper: Click Actuaciones tab
  │   │
  │   ├─► web_scraper: Extract first row
  │   │   └─► [Date, Action, Court, Type, Doc, Note]
  │   │
  │   ├─► web_scraper: Click Sujetos Procesales
  │   │
  │   ├─► web_scraper: Extract demandante/demandado
  │   │   └─► ["Juan Perez", "Maria Garcia"]
  │   │
  │   ├─► excel_operations: Write all data
  │   │   └─► Updated Excel file:
  │   │       A: Demandante
  │   │       B: Demandado
  │   │       C: Despacho
  │   │       E-J: Actuaciones
  │   │
  │   └─► Close browser, move to next
  │
  └─► END
      Logs created, Excel saved, Done!
```

## File Dependency Graph

```
main.py
├── Imports from config
│   ├── logger (used everywhere)
│   ├── LOG_FILE_PATH (displayed at end)
│   └── URL, EXCEL_FILE_PATH (passed to modules)
│
├── Imports from excel_operations
│   ├── read_numbers_from_excel()
│   ├── write_data_to_excel()
│   ├── write_despacho_to_excel()
│   └── write_sujetos_to_excel()
│
├── Imports from web_driver
│   └── access_url()
│
└── Imports from web_scraper
    ├── select_second_radio_button()
    ├── enter_search_number()
    ├── click_consultar_button()
    ├── click_volver_button()
    ├── click_first_clickable_table_number()
    ├── click_actuaciones_tab()
    ├── print_actuaciones_first_row()
    ├── extract_despacho_value()
    ├── click_subjetos_procesales_tab()
    └── extract_subjetos_procesales()

excel_operations depends on:
├── config (logger, EXCEL_FILE_PATH)
└── openpyxl library

web_driver depends on:
├── config (URL, logger)
└── selenium library

web_scraper depends on:
├── config (logger)
├── selenium library
├── time module
└── re module
```

## Code Size Summary

```
Module                    Lines    Responsibility
─────────────────────────────────────────────────────
main.py                    110     Orchestration
config.py                   60     Configuration
web_driver.py               35     Browser setup
excel_operations.py        150     Excel I/O
web_scraper.py             650     Web interaction
─────────────────────────────────────────────────────
TOTAL CODE              ~1,005     lines
─────────────────────────────────────────────────────

Documentation            Lines     Purpose
─────────────────────────────────────────────────────
README.md                ~180     Architecture
QUICKSTART.md            ~150     Getting started
DEVELOPMENT.md           ~250     Adding features
LOGGING.md               ~150     Troubleshooting
REFACTORING_SUMMARY.md   ~200     What changed
─────────────────────────────────────────────────────
TOTAL DOCS              ~930      lines
```

## Execution Timeline

```
0:00  ┌─ Script starts
      │
0:01  ├─ Excel loaded, numbers read
      │
0:02  ├─ Browser opens
      ├─ Fill form: Demandante/Demandado
      ├─ Search & extract Despacho    (~12 sec)
      ├─ Switch to Actuaciones tab
      ├─ Extract first row
      ├─ Switch to Sujetos Procesales
      ├─ Extract names
      ├─ Write to Excel
      ├─ Close browser
      │
0:14  ├─ First number complete
      │
      ├─ (repeat for each number)
      │
3:00  ├─ All 10 numbers done
      │
      ├─ Logs saved
      ├─ Excel updated
      │
3:01  └─ Script ends
```

## Module Responsibilities

```
┌─────────────────────────────────────────────────────┐
│                   main.py                            │
│            Orchestrates workflow                     │
│     (The conductor - doesn't do actual work)        │
└────────┬────────────────────────────────────────────┘
         │
    ┌────┴──────┬──────────────┬──────────────┐
    │            │              │              │
    ▼            ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐
│config  │  │excel     │  │web_driver│  │web_scraper  │
│        │  │          │  │          │  │             │
│Setup & │  │Read/Write│  │Open      │  │Click/Extract│
│Config  │  │Excel     │  │Browser   │  │Web Data     │
└────────┘  └──────────┘  └──────────┘  └─────────────┘
```

## How to Navigate the Code

1. **Want to understand the flow?**
   - Read main.py (110 lines, very clear)

2. **Want to modify Excel operations?**
   - Edit excel_operations.py

3. **Want to modify web interactions?**
   - Edit web_scraper.py

4. **Want to change logging?**
   - Edit config.py

5. **Want to change browser setup?**
   - Edit web_driver.py

## Documentation Map

```
START HERE
    ↓
QUICKSTART.md ─────────┐
(5 min read)           │
    │                  ├─► Run: python main.py
    └─────────────────┘
                       
         Check Results
              ↓
    LOGGING.md ◄──────┬── If errors
    (Troubleshoot)    │
                      └─► See logs/
         
     Understand Code
              ↓
    README.md ◄───────── Architecture
    (20 min)
         
        Add Features
              ↓
    DEVELOPMENT.md ◄──── Guidelines
    (Implementation)
         
     What Changed?
              ↓
    REFACTORING_SUMMARY.md
```

## Statistics

```
Original: 1 file (main.py, 965 lines)
├─ Mixed concerns
├─ Hard to navigate
├─ Difficult to extend

Refactored: 5 focused modules (1005 lines)
├─ Separated concerns
├─ Easy to navigate
├─ Simple to extend

Documentation: 5 guides (930 lines)
├─ Comprehensive
├─ Well organized
├─ Examples included

Total: 1,935 lines of code & docs
```

## Quick Navigation

| Need | File | Lines |
|------|------|-------|
| Run script | main.py | 110 |
| Get started | QUICKSTART.md | 150 |
| Understand | README.md | 180 |
| Develop | DEVELOPMENT.md | 250 |
| Debug | LOGGING.md | 150 |
| Config | config.py | 60 |
| Excel | excel_operations.py | 150 |
| Browser | web_driver.py | 35 |
| Scrape | web_scraper.py | 650 |

All organized, documented, and ready to use!
