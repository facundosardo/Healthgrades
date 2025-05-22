import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # For headless mode

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    master_file = "healthgrades_ac.csv"
    new_file = "healthgrades_acnewprofs.csv"

    # Read existing professionals from the master file to avoid duplicates
    existing_pros = set()
    if os.path.exists(master_file):
        with open(master_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                # Use name+city as unique key
                if len(row) >= 2:
                    key = (row[0], row[1])
                    existing_pros.add(key)

    new_pros = []
    all_pros = []

    try:
        driver.get("https://www.healthgrades.com/")

        # Search for 'Acupuncture'
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "home-search-input")))
        search_input.clear()
        search_input.send_keys("Acupuncture")

        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button._5qxNR[data-qa-target='home-form-search-btn']")
        ))
        search_button.click()
        print("Initial search with 'Acupuncture' done.")

        # Write location
        location_input = wait.until(EC.element_to_be_clickable((By.ID, "synd-header-location-input")))
        driver.execute_script("arguments[0].value = '';", location_input)
        location_input.click()
        for _ in range(20):
            location_input.send_keys(Keys.BACKSPACE)
            time.sleep(0.05)
        location_input.send_keys("Fairfield, CT")

        time.sleep(1)

        try:
            suggestions_ul = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "ul[role='listbox']")
            ))
            first_option = suggestions_ul.find_element(By.TAG_NAME, "li")
            first_option.click()
            print("First suggestion option selected.")
        except Exception:
            print("Suggestion list did not appear or could not be selected, continuing without selection.")

        # Click final search button
        final_search_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@aria-label, 'Fairfield, CT') and contains(@aria-label, 'Search for Acupuncture')]"
        )))
        final_search_btn.click()
        print("Final search button clicked.")

        time.sleep(5)

        while True:
            profiles = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                "h3[data-qa-target='provider-name']"
            )))
            print(f"Found {len(profiles)} professionals on current page.")

            for profile_h3 in profiles:
                try:
                    name = profile_h3.find_element(By.CSS_SELECTOR, "a[data-qa-target='name-link']").text.strip()

                    parent_container = profile_h3.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MUU7qPwXH8scbrT7')]")
                    addresses = parent_container.find_elements(By.TAG_NAME, "address")

                    full_address = ""
                    for addr in addresses:
                        text = addr.text.strip()
                        if text:
                            full_address = text
                            break

                    if not full_address:
                        full_address = "No address"

                    lines = full_address.split("\n")
                    if len(lines) > 1:
                        city = lines[1].strip()
                    else:
                        city = full_address.strip()

                    key = (name, city)

                    if key not in existing_pros:
                        print(f"New professional detected: {name} - {city}")
                        existing_pros.add(key)
                        new_pros.append([name, city, full_address])

                    all_pros.append([name, city, full_address])

                except Exception as e:
                    print(f"Error extracting data from a profile: {e}")
                    continue

            # Pagination
            try:
                next_button = wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//a[@data-qa-target='pagination--next-page' and @aria-label='Next Page']"
                )))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(0.5)
                next_button.click()
                print("Moving to next page...")
                wait.until(EC.staleness_of(profiles[0]))
                wait.until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "h3[data-qa-target='provider-name']"
                )))
            except Exception:
                print("No next page button found or last page reached.")
                break

        # Save master file (all professionals)
        with open(master_file, "w", newline="", encoding="utf-8") as f_master:
            writer_master = csv.writer(f_master)
            writer_master.writerow(["Name", "City", "Full Address"])
            writer_master.writerows(all_pros)

        # Save new professionals only
        with open(new_file, "w", newline="", encoding="utf-8") as f_new:
            writer_new = csv.writer(f_new)
            writer_new.writerow(["Name", "City", "Full Address"])
            writer_new.writerows(new_pros)

        print(f"Master file updated with {len(all_pros)} professionals.")
        print(f"{len(new_pros)} new professionals saved in '{new_file}'.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
