import time
import csv
import os 
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def set_location_strict(driver, wait, location_input, location_text="Fairfield, CT", max_attempts=10):
    for attempt in range(max_attempts):
        try:
            # Focus and clear via JS and keyboard
            driver.execute_script("arguments[0].focus();", location_input)
            driver.execute_script("arguments[0].value = '';", location_input)
            time.sleep(0.2)

            # Select all and delete (Cmd/Ctrl + A + Backspace)
            if platform.system() == "Darwin":
                location_input.send_keys(Keys.COMMAND, "a")
            else:
                location_input.send_keys(Keys.CONTROL, "a")
            time.sleep(0.1)
            location_input.send_keys(Keys.BACKSPACE)
            time.sleep(0.2)

            # Send the correct location text
            location_input.send_keys(location_text)
            time.sleep(0.5)

            # Trigger input event manually to ensure front-end registers it
            driver.execute_script("""
                var input = arguments[0];
                var lastValue = input.value;
                input.value = '';
                input.value = lastValue;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            """, location_input)
            time.sleep(0.5)

            # Check value
            val = driver.execute_script("return arguments[0].value;", location_input)
            if val.strip().lower() == location_text.lower():
                print(f"Location set successfully on attempt {attempt+1}")
                return
            else:
                print(f"Attempt {attempt+1}: Location input value is '{val}', retrying...")
        except Exception as e:
            print(f"Attempt {attempt+1}: Exception during setting location: {e}")

    raise Exception(f"Failed to set location input to '{location_text}' after {max_attempts} attempts")

def scrape_profession(profession):
    master_file = "healthgrades_master.csv"
    new_file = "healthgrades_new.csv"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment if you want headless

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    existing_pros = set()
    all_pros = []

    if os.path.exists(master_file):
        with open(master_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    key = (row[0], row[1])
                    existing_pros.add(key)
                    all_pros.append([row[0], row[1], row[2] if len(row) > 2 else "No address"])

    new_pros = []

    try:
        driver.get("https://www.healthgrades.com/")

        search_input = wait.until(EC.element_to_be_clickable((By.ID, "home-search-input")))
        search_input.clear()
        search_input.send_keys(profession)

        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button._5qxNR[data-qa-target='home-form-search-btn']")
        ))
        search_button.click()
        print(f"Initial search with '{profession}' done.")

        location_input = wait.until(EC.element_to_be_clickable((By.ID, "synd-header-location-input")))

        set_location_strict(driver, wait, location_input, "Fairfield, CT")

        try:
            suggestions_ul = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "ul[role='listbox']")
            ))
            first_option = suggestions_ul.find_element(By.TAG_NAME, "li")
            first_option.click()
            print("First suggestion option selected.")
        except Exception:
            print("Suggestion list did not appear or could not be selected, continuing without selection.")

        try:
            # Wait for overlay to disappear if any
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "span._overlay_1ox12_70")))
        except:
            pass

        final_search_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//button[contains(@aria-label, 'Fairfield, CT') and contains(@aria-label, 'Search for {profession}')]"
        )))

        try:
            final_search_btn.click()
        except Exception:
            # If click intercepted, click via JS
            driver.execute_script("arguments[0].click();", final_search_btn)

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

    finally:
        driver.quit()

    # Save new professionals only
    with open(new_file, "w", newline="", encoding="utf-8") as f_new:
        writer_new = csv.writer(f_new)
        writer_new.writerow(["Name", "City", "Full Address"])
        writer_new.writerows(new_pros)

    # Save master file only if new professionals found
    if new_pros:
        with open(master_file, "w", newline="", encoding="utf-8") as f_master:
            writer_master = csv.writer(f_master)
            writer_master.writerow(["Name", "City", "Full Address"])
            writer_master.writerows(all_pros)
        print(f"Master file updated with {len(all_pros)} professionals.")
    else:
        print("No new professionals found; master file not updated.")

    print(f"{len(new_pros)} new professionals saved in '{new_file}'.")

def main():
    for profession in ["Acupuncture", "Chiropractic", "Massage Therapy", "Neuropathology"]:
        scrape_profession(profession)

if __name__ == "__main__":
    main()
