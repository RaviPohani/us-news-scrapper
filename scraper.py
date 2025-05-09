import requests
from bs4 import BeautifulSoup
import pandas as pd

infra_types = {
    'Transport': ['road', 'rail', 'airport', 'bridge', 'highway'],
    'Energy': ['solar', 'wind', 'hydro', 'power', 'grid', 'electric'],
    'Water': ['water', 'wastewater', 'sewage', 'pipeline'],
    'Digital': ['fiber', 'data center', '5G', 'broadband']
}

deal_types = {
    'M&A': ['acquire', 'acquisition', 'merger', 'buyout'],
    'Greenfield': ['new project', 'greenfield', 'groundbreaking'],
    'Brownfield': ['brownfield', 'redevelopment', 'upgrade'],
    'PPP': ['PPP', 'P3', 'public-private partnership']
}

delivery_methods = ['DBFOM', 'EPC', 'Lease', 'O&M']

def classify_category(text, categories):
    for category, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                return category
    return 'Uncategorized'

def classify_delivery_method(text):
    for method in delivery_methods:
        if method.lower() in text.lower():
            return method
    return 'N/A'

def scrape_enr():
    response = requests.get('https://www.enr.com/articles/topic/442-infrastructure')
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    for item in soup.find_all('div', class_='listing__content'):
        title_tag = item.find('a', class_='listing__title')
        date_tag = item.find('div', class_='listing__date')
        if title_tag and date_tag:
            title = title_tag.text.strip()
            link = 'https://www.enr.com' + title_tag['href']
            date = date_tag.text.strip()
            infra_type = classify_category(title, infra_types)
            deal_type = classify_category(title, deal_types)
            delivery_method = classify_delivery_method(title)
            articles.append({
                'Date of Article': date,
                'Infrastructure Type': infra_type,
                'Deal Type': deal_type,
                'Infrastructure Delivery Method': delivery_method,
                'Title of article': title,
                'Link of article': link
            })
    return pd.DataFrame(articles)
