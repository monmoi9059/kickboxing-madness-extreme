from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

print("Setup Chrome options...")
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    print("Initialize WebDriver...")
    driver = webdriver.Chrome(options=options)

    print("Load file...")
    file_path = f"file://{os.path.abspath('EFLTG.html')}"
    driver.get(file_path)
    time.sleep(1) # Allow load time

    print("Checking console logs for errors...")
    logs = driver.get_log('browser')
    errors = [log for log in logs if log['level'] == 'SEVERE']

    if errors:
        print("Found errors:")
        for e in errors:
            print(e)
    else:
        print("No severe errors found in browser console.")

    driver.quit()
    print("Test finished successfully.")
except Exception as e:
    print(f"Error running test: {e}")
