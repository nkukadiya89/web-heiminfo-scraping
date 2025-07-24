import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_window_size(1920, 1080)

driver.get("https://www.heiminfo.ch/institutionen")
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.institution")))

soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all("article", class_="institution")

all_data = []
print(f"Found {len(articles)} institutions.")

for idx, art in enumerate(articles, 1):
    h2 = art.select_one("h2")
    if not h2:
        continue

    company = h2.get_text(strip=True)
    zip_code = art.select_one(".plz").get_text(strip=True) if art.select_one(".plz") else "N/A"
    city = art.select_one(".city").get_text(strip=True) if art.select_one(".city") else "N/A"
    inst_type = art.get("data-institution-type", "N/A")
    detail_url = "https://www.heiminfo.ch" + art.select_one("a")["href"]

    driver.get(detail_url)
    time.sleep(2)

    email = phone = website = name = surname = function = address = "N/A"

    current_url = driver.current_url
    if "admin.heiminfo.ch" in current_url:
        print(f"[{idx}] 🔒 Redirected to admin – no contact details for: {company}")
    else:
        detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

        def get_text(sel):
            t = detail_soup.select_one(sel)
            return t.get_text(strip=True) if t else "N/A"

        def get_href(sel):
            t = detail_soup.select_one(sel)
            return t.get('href', '').split("?")[0].strip() if t else "N/A"

        email = get_href('a[href^="mailto:"]')
        phone = get_href('a[href^="tel:"]')
        website = get_href('a[target="_blank"][href^="http"]')
        name = get_text(".field-name span")
        surname = get_text(".field-surname span")
        function = get_text(".field-position span")
        address = get_text(".address")

    all_data.append([
        company, address, zip_code, city, "Switzerland",
        inst_type, website, name, surname, function, email, phone
    ])

if all_data:
    fname = "institutions_data.csv"
    with open(fname, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Company", "Address", "Zip Code", "City", "Country",
            "Type of Institution", "Website", "Name", "Surname",
            "Function", "Email", "Phone"
        ])
        writer.writerows(all_data)
    print(f"\nSaved {len(all_data)} records to '{fname}'")
else:
    print("\nNo data saved.")

driver.quit()