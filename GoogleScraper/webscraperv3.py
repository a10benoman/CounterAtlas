import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

base_url = 'https://cse.google.com/cse?cx=a3240aae15a61423c#gsc.tab=0'
visited_links = set()
links_to_visit = [base_url]
page_count = 0
max_pages = 1000
unique_emails = set()

def scrape_emails(html):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_regex, html)
    emails = set(matches)
    return emails

def scrape_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # find all <a> tags
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            parsed_href = urlparse(href)
            if parsed_href.netloc == '':
                href = base_url + href
                parsed_href = urlparse(href)
            if parsed_href.scheme == 'http' or parsed_href.scheme == 'https':
                if parsed_href.netloc.endswith(urlparse(base_url).netloc) and href not in visited_links:
                    links.append(href)

    return links

try:
    while links_to_visit and page_count < max_pages:
        url = links_to_visit.pop(0)
        if url not in visited_links:
            visited_links.add(url)
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                emails = scrape_emails(html)
                unique_emails.update(emails)
                links = scrape_links(html)
                links_to_visit.extend(links)
                page_count += 1
                print(f'Scraped {url} : {", ".join(emails)}')
            else:
                print(f'Request failed for {url}')
        else:
            pass
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    print(f'Total pages scraped: {page_count}')
    print(f'Total unique emails found: {len(unique_emails)}')
    print('Unique emails found: ', end='')
    print(', '.join(unique_emails))
