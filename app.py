from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    url = request.form['url']

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

    soup = BeautifulSoup(driver.page_source, "html.parser")
    anchor_tags = soup.find_all("a")
    inner_urls = [tag["href"] for tag in anchor_tags]

    data = []
    base_url = driver.current_url
    for i in range(len(inner_urls)):
        source_url = inner_urls[i]
        for j in range(i + 1, len(inner_urls)):
            target_url = inner_urls[j]
            absolute_source_url = urljoin(base_url, source_url)
            absolute_target_url = urljoin(base_url, target_url)
            response = requests.get(absolute_source_url)
            response_time = response.elapsed.total_seconds()

            source_name = source_url.split("/")[-1] if source_url.endswith("/") else source_url.split("/")[-1].split(".")[0]
            target_name = target_url.split("/")[-1] if target_url.endswith("/") else target_url.split("/")[-1].split(".")[0]

            data.append({"Source URL": source_url, "Source Name": source_name,
                         "Target URL": target_url, "Target Name": target_name,
                         "Response Time (s)": response_time})

    df = pd.DataFrame(data)
    print

    output_file = "outpt.xlsx"
    df.to_excel(output_file, index=False)

    driver.quit()

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run()
