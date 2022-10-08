import pandas as pd
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os

def get_page(url):
    res = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(res, 'html.parser', from_encoding=res.info().get_param('charset'))
    return soup

def get_sitemaps(robot_file):
    data = []
    lines = str(robot_file).splitlines()
    for line in lines:
        if line.startswith('Sitemap:'):
            split = line.split(':', maxsplit=1)
            data.append(split[1].strip())
    return data

def to_dataframe(robot_file):
    data = []
    lines = str(robot_file).splitlines()
    for line in lines:
        if line.strip():
            if not line.startswith('#'):
                split = line.split(':', maxsplit=1)
                data.append([split[0].strip(), split[1].strip()])
    return pd.DataFrame(data, columns=['directive', 'parameter'])

url = "https://www.google.com/robots.txt"
url_base = urlparse(url).netloc
url_base = ('.'.join(url_base.split('.')[-2:]))
url_base = url_base.split('.')[0]
robots = get_page(url)
sitemaps = get_sitemaps(robots)

df = to_dataframe(robots)
df.head(10)
csv_file_name = str(url_base)

if os.path.isdir('Data'):
    df.to_csv('Data/'+csv_file_name + '-robots.csv')
else:
    os.mkdir('Data')
    df.to_csv('Data/'+csv_file_name+'-robots.csv')

sitemap_link = df[df['directive'] == 'Sitemap']
website_links = df[df['directive'] == 'Allow']