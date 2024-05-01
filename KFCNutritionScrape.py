# LOAD LIBRARIES
from playwright.sync_api import sync_playwright
import time
import datetime
import csv

now = datetime.datetime.now()
today = datetime.date.today()

URL = 'https://www.kfc.com.au/nutrition-allergen'

# Initial Run to set up CSV file
header = ['Name', 'Average serving size (g)', 'Energy (kJ)', 'Protein (g)', 'Fat, total (g)', 'Fat, saturated (g)', 'Carbohydrate (g)', 'Carbohydrate, sugars (g)', 'Sodium (mg)']

with open(f'{today}KFCNutrition.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)



# LOAD UP AUTOMATED BROWSER
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)

    time.sleep(5)

    # Accounting for dynamic content to be loaded, goal is slowly scroll to the bottom
    for i in range(1,50):
        page.keyboard.press('PageDown')
        time.sleep(0.5)

    # Scrapper will obtain all 'MORE INFO' clickable links. Then is looped through all by loading up a popup box with the desired information and closes box before loading up next
    links = page.query_selector_all('div.more-info')
    print(len(links))

    for link in links:
        link.click()

        time.sleep(3)

        name = page.query_selector('div.product-name')
        print(name.text_content())

        # Name of product + all nutrition values are obtained
        results = []

        results.append(name.text_content())

        # NUTRITION INFO OBTAIN #
        for j in range(1,9):
            nut_selector = f'div.nutrition-name-amoumt-details:nth-child({j}) > div:nth-child(1)'
            nut_info = page.query_selector(nut_selector)
            # print(nut_info.text_content())
            results.append(nut_info.text_content())

        print(results)

        # Append data to CSV
        with open(f'{today}KFCNutrition.csv', 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(results)

        close_button = page.query_selector('.custom-modal-close').click()

        time.sleep(3)

    browser.close()

print("OPERATION COMPLETE")
print(now)
