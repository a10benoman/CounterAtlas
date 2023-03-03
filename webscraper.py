import re
import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://www.jsa.org'
visited_links = set()
links_to_visit = [base_url]
emails = set()
page_count = 0
max_pages = 500

def scrape_emails(html):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_regex, html)
    for match in matches:
        emails.add(match)

def scrape_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # find all <a> tags
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href not in visited_links:
            links.append(href)

    # find all <button> tags
    for button in soup.find_all('button'):
        onclick = button.get('onclick')
        if onclick and 'location.href' in onclick:
            href = re.search(r"'(.+?)'", onclick).group(1)
            if href and href not in visited_links:
                links.append(href)

    # find all hidden links
    for input_ in soup.find_all('input'):
        input_type = input_.get('type')
        if input_type == 'hidden':
            value = input_.get('value')
            if value and value.startswith('http'):
                if value not in visited_links:
                    links.append(value)

    return links

try:
    while links_to_visit and page_count < max_pages:
        url = links_to_visit.pop(0)
        visited_links.add(url)
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            scrape_emails(html)
            links = scrape_links(html)
            links_to_visit.extend(links)
            page_count += 1
            print(f'Scraped {url}')
        else:
            print(f'Request failed for {url}')
except KeyboardInterrupt:
    print('Program interrupted. Saving current state...')
    state = {
        'visited_links': list(visited_links),
        'links_to_visit': links_to_visit,
        'emails': list(emails),
        'page_count': page_count
    }
    with open('state.json', 'w') as f:
        json.dump(state, f)
    print('State saved. Exiting program.')
    
    print(f'Visited {page_count} pages')
    print(f'Total unique emails found: {len(emails)}')
    print('Unique emails:')
    for email in emails:
        print(email)

print(f'Visited {page_count} pages')
print(f'Total unique emails found: {len(emails)}')
print('Unique emails:')
for email in emails:
    print(email)
