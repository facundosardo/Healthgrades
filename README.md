# 📝 Healthgrades Scraper  

This script extracts healthcare professional data from **Healthgrades**, focusing on Acupuncture, Chiropractic, and Massage Therapy in Fairfield, CT. It saves data into two CSV files per profession:  

---

## 📁 **Generated Files**  
- **healthgrades_xx.csv:** Master database with all collected professionals (no duplicates).  
- **healthgrades_xxnewprofs.csv:** Only new professionals found in the current run.  

(`xx` suffix: `ac` for Acupuncture, `ch` for Chiropractic, `ma` for Massage Therapy)  

---

## ⚙️ **Requirements**  
- Python 3.x  
- Google Chrome  
- Packages:  
    ```bash
    pip install selenium webdriver-manager
    ```  

---

## 🚀 **Usage**  
1. Clone or download the script.  
2. Install dependencies.  
3. Run the script:  
    ```bash
    python your_script.py
    ```  
   (Runs all three professions automatically)  

---

## 🌐 **How it works**  
- Opens Healthgrades homepage.  
- Inputs profession and sets location to "Fairfield, CT" (clearing previous input).  
- Searches and navigates all result pages.  
- Extracts Name, City, and Full Address of professionals.  
- Saves all data in a master CSV and new entries in a separate CSV.  
- Avoids duplicates using (Name, City) as a unique key.  

---

## 🤖 **Customization**  
Modify the profession and file names in the `scrape_profession()` calls.  
Enable headless mode by uncommenting the option in the script.  

---

## 📌 **Notes**  
- Browser opens maximized by default.  
- Keep Chrome and ChromeDriver updated for compatibility.  

---

## 🙌 **Contributions**  
Feel free to open issues or pull requests for improvements or help.