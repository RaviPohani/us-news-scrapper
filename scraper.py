import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# USDOT Newsroom URL
url = 'https://www.transportation.gov/newsroom'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# List to store news
articles = []

# Loop through news article listings
for row in soup.find_all('div', class_='views-row'):
    try:
        title_tag = row.find('h3')
        if title_tag:
            title = title_tag.text.strip()
            link = 'https://www.transportation.gov' + title_tag.find('a')['href']
        else:
            continue

        # Extract date
        date_tag = row.find('span', class_='date-display-single')
        date = date_tag.text.strip() if date_tag else datetime.now().strftime('%Y-%m-%d')

        # Classify infrastructure type based on keywords
        if 'aviation' in title.lower() or 'airport' in title.lower():
            infra_type = 'Aviation'
        elif 'rail' in title.lower() or 'amtrak' in title.lower():
            infra_type = 'Rail'
        elif 'highway' in title.lower() or 'bridge' in title.lower():
            infra_type = 'Road/Bridge'
        elif 'port' in title.lower() or 'maritime' in title.lower():
            infra_type = 'Port/Maritime'
        else:
            infra_type = 'General Transport'

        deal_type = 'Announcement'
        delivery_method = 'Public Funding'

        articles.append({
            'Date of Article': date,
            'Infrastructure Type': infra_type,
            'Deal Type': deal_type,
            'Infrastructure Delivery Method': delivery_method,
            'Title of Article': title,
            'Link of Article': link
        })
    except Exception as e:
        print(e)

# Convert to DataFrame
df = pd.DataFrame(articles)

# Export to Excel
df.to_excel('usdot_infra_news.xlsx', index=False)
print("✅ Data exported to 'usdot_infra_news.xlsx'")
