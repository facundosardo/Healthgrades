# 📝 Healthgrades Scraper  

This script extracts healthcare professional data from **Healthgrades**, focusing on Acupuncture, Chiropractic, and Massage Therapy in Fairfield, CT. It saves data into two CSV files per profession:  

---

## 📁 **Generated Files**  
- **healthgrades_xx.csv:** Master database containing all collected professionals (no duplicates).  
- **healthgrades_xxnewprofs.csv:** Contains only new professionals found in the current run.  

(`xx` suffixes:  
- `ac` for Acupuncture  
- `ch` for Chiropractic  
- `ma` for Massage Therapy)  

---

## ⚙️ **Requirements**  
- Python 3.x  
- Google Chrome browser  
- Python packages:  
    ```bash
    pip install selenium webdriver-manager
    ```  

---

## 🚀 **Usage**  
1. Clone or download the repository or script.  
2. Install dependencies as shown above.  
3. Run the script:  
    ```bash
    python your_script.py
    ```  
   (This will run all three professions sequentially.)  

---

## 🌐 **How it works**  
- Opens the Healthgrades homepage.  
- Enters the profession keyword and sets location to "Fairfield, CT" (clearing previous input completely).  
- Executes the search and navigates through all result pages.  
- Extracts each professional’s Name, City, and Full Address.  
- Saves all results to a master CSV file and only new entries to a separate CSV file.  
- Uses (Name, City) as a unique key to avoid duplicates.  

---

## 🤖 **Customization**  
- To scrape other professions or locations, modify the `scrape_profession()` function calls with desired keywords and file names.  
- Headless mode can be enabled by uncommenting the respective option in the script.  

---

## 📌 **Notes**  
- The browser opens maximized by default to reduce scraping errors.  
- Ensure your Chrome and ChromeDriver versions are compatible to avoid issues.  

---

## 🙌 **Contributions**  
Contributions, bug reports, and feature requests are welcome. Feel free to open issues or pull requests.
