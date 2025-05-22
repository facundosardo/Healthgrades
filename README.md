# Healthgrades Professionals Scraper

This repository contains three Python scripts to scrape health professionals data from [Healthgrades](https://www.healthgrades.com/). Each script targets a different profession and generates CSV files with the extracted information.

---

## File Structure

- `healthgrades_ac.py`  
  Scrapes **Acupuncture** professionals in Fairfield, CT.

- `healthgrades_chiropractic.py`  
  Scrapes **Chiropractic** professionals in Fairfield, CT.

- `healthgrades_massage.py`  
  Scrapes **Massage Therapy** professionals in Fairfield, CT.

---

## General Workflow

Each script performs the following steps:

1. Opens the Healthgrades homepage.  
2. Inputs the search term for the specific profession.  
3. Sets the location to **Fairfield, CT**, replacing the default location.  
4. Executes the search and navigates through all result pages.  
5. Extracts for each professional:  
   - Name  
   - City  
   - Full address  
6. Saves the data into two CSV files:

| File                 | Content                                        |
|----------------------|------------------------------------------------|
| `healthgrades_xx.csv`        | Master cumulative database without duplicates. |
| `healthgrades_xxnewprofs.csv` | New professionals found in the current run.      |

**Note:** `xx` suffix depends on the profession:  
- `ac` for Acupuncture  
- `ch` for Chiropractic  
- `ma` for Massage Therapy

---

## Requirements

- Python 3.x  
- Installed packages:  
  - selenium  
  - webdriver-manager  

Quick install command:  
```bash
pip install selenium webdriver-manager
```

## Usage

Run any of the scripts:

```bash
Copy
python healthgrades_ac.py
python healthgrades_chiropractic.py
python healthgrades_massage.py
```

## Notes

- The scraper avoids duplicates using (Name, City) as a unique key.
- CSV files are updated to maintain a historical master file and a separate file for new entries only.
- Browser opens maximized; headless mode can be enabled by uncommenting the respective line in the scripts.
- ChromeDriver and browser versions should be compatible to avoid issues.

## Contributions

Feel free to open issues or pull requests for improvements or bug fixes.