import requests
from bs4 import BeautifulSoup

# Send a request to the URL
url = 'https://cse.google.com/cse?cx=a3240aae15a61423c#gsc.tab=0&gsc.q=connect&gsc.sort='
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all the <a> tags with class 'gs-title' and store their text in a list
gs_titles = [tag.text for tag in soup.find_all('a', class_='gs-title')]

# Print all the gs titles
print("\n".join(gs_titles))
