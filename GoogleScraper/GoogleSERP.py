import csv
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
     
def simpleGoogleSearch(query, start):
    results = []

    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}&start={start}"

    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
  
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')

            if anchors:
                link  = anchors[0]['href']
                title = g.find('h3').text
                item  = {"title": title, "link": link}
                results.append(item)

    return results
     

def googleToPandas(googleQuery):
    resultsCounter  = 0
    resultsList     = []

    while True:
        pageResults = simpleGoogleSearch(googleQuery, resultsCounter)
        
        if not pageResults:
            break
        else: 
            resultsList.extend(pageResults)
            resultsCounter = resultsCounter + 10

    return pd.DataFrame(resultsList)


googleSearchQuery = 'site:jsa.org "accounts"'
results = googleToPandas(googleSearchQuery)

# Save results to CSV file
script_path = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_path, 'google_search_results.csv')

print(f"Output file path: {output_file}")
print(f"Current directory: {os.getcwd()}")

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])
    for result in results.itertuples():
        writer.writerow([result.title, result.link])

print(f"Results saved to {output_file}")
