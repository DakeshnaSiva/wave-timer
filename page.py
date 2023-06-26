import requests
from bs4 import BeautifulSoup
import pandas as pd

url = input("Enter the url:")

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

page_links = soup.find_all('a')


inner_links = []
for link in page_links:
    href = link.get('href')
    if href and not href.startswith('javascript:'):
        inner_links.append((link.text.strip(), href))

data = pd.DataFrame(inner_links, columns=['Link Name', 'URL'])
data['wave Time (s)'] = None


for i, row in data.iterrows():
    link_name = row['Link Name']
    link_url = row['URL']
    
    if not link_url.startswith('http'):
        link_url = url + link_url  
    
    
    try:
        response = requests.get(link_url)
        response_time = response.elapsed.total_seconds()  
        
        data.loc[i, 'wave Time (s)'] = response_time
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching URL: {link_url}")
        print(f"Error message: {str(e)}")
        data.loc[i, 'wave Time (s)'] = 'Error'


data.to_excel('time.xlsx', index=False)
print("data insert sucessfully")