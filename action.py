from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

username = input("Enter your username: ")
password = input("Enter your password:")
url = input("Enter the URL: ")

driver = webdriver.Chrome()

driver.get(url)


username_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "username"))
)

password_field = driver.find_element(By.NAME, "password")

username_field.send_keys(username)
password_field.send_keys(password)


form_element = username_field.find_element(By.XPATH, "./ancestor::form")

submit_button = form_element.find_element(By.XPATH, "//button[@type='submit']")

submit_button.click()

time.sleep(5)  

# Extract the inner URLs
soup = BeautifulSoup(driver.page_source, "html.parser")
anchor_tags = soup.find_all("a")
inner_urls = [tag["href"] for tag in anchor_tags]


data = []
base_url = driver.current_url  # Get the base URL from the current page
for url in inner_urls:
    absolute_url = urljoin(base_url, url)  # Convert relative URL to absolute URL
    response = requests.get(absolute_url)
    response_time = response.elapsed.total_seconds()
    data.append({"Url actions": absolute_url, "Response Time (s)": response_time})

df = pd.DataFrame(data)
print(df)


output_file = "response_times.xlsx"
df.to_excel(output_file, index=False)

print("Data saved to", output_file)


driver.quit()
