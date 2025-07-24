# Heiminfo.ch Institution Scraper
 
This Python script scrapes institutional contact data from [heiminfo.ch](https://www.heiminfo.ch/institutionen), a Swiss directory for social and healthcare institutions. It collects detailed information from the main listings and individual institution pages and saves it into a structured CSV file.
 
---
 
## 📌 Features
 
- Uses **Selenium** with **BeautifulSoup** for dynamic and static scraping.
- Runs Chrome in **headless** mode (no GUI).
- Extracts:
  - Institution Name
  - Address, Zip Code, City
  - Institution Type
  - Website, Email, Phone
  - Contact Person's Name, Surname, and Function
- Skips admin pages that don't reveal contact data.
- Saves all results to `institutions_data.csv`.
 
---
 
##  Requirements
 
Install dependencies using pip:

pip install selenium beautifulsoup4 webdriver-manager