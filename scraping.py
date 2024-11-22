from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.sharesansar.com/index-history-data')

wait = WebDriverWait(driver, 15)

from_date = "2000-01-01"
to_date = "2024-01-01"

from_date_field = wait.until(EC.presence_of_element_located((By.ID, 'fromDate')))
to_date_field = wait.until(EC.presence_of_element_located((By.ID, 'toDate')))

from_date_field.clear()
from_date_field.send_keys(from_date)

to_date_field.clear()
to_date_field.send_keys(to_date)

search_button = driver.find_element(By.ID, 'btn_indxhis_submit')
search_button.click()

wait.until(EC.presence_of_element_located((By.ID, 'myTable')))

all_data = []

for page in range(1, 288):
    wait.until(EC.presence_of_element_located((By.ID, 'myTable')))
    
    rows = driver.find_elements(By.CSS_SELECTOR, '#myTable tbody tr')

    for row in rows:
        try:
            columns = row.find_elements(By.CSS_SELECTOR, 'td')
            data = [col.text.strip() for col in columns]
            all_data.append(data)
        except Exception as e:
            print(f"Error retrieving data from row: {e}")
    
    try:
        next_button = driver.find_element(By.ID, 'myTable_next')
        if 'disabled' in next_button.get_attribute('class'):
            break
        next_button.click()
        time.sleep(3)
    except Exception as e:
        print(f"Error clicking next button: {e}")
        break

columns = ['S.N.', 'Open', 'High', 'Low', 'Close', 'Change', 'Per Change (%)', 'Turnover', 'Date']

df = pd.DataFrame(all_data, columns=columns)

df.to_csv('nepse_index_data.csv', index=False)

driver.quit()
