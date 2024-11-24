from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
url = "https://www.cardmarket.com/fr/Pokemon/Products"
driver.get(url)

# Get the rendered HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find the elements
data = {}
for dt, dd in zip(soup.find_all('dt', class_='col-6 col-xl-5'), soup.find_all('dd', class_='col-6 col-xl-7')):
    label = dt.get_text(strip=True)
    value = dd.get_text(strip=True)
    data[label] = value

# Print the prices
for key, value in data.items():
    if "Prix" or "de" in key:
        print(f"{key}: {value}")

driver.quit()