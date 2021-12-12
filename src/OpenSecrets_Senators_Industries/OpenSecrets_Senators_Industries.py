import requests
import json
from json.decoder import JSONDecodeError
import pandas as pd
from bs4 import BeautifulSoup

def test():
    return 'test'

def top_20_industries():
    url = 'https://www.opensecrets.org/federal-lobbying/industries'
    html = requests.get(url)
    df = pd.read_html(html.text)
    return df

def top_20_industries_ids():
    url = 'https://www.opensecrets.org/federal-lobbying/industries'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    url_ids = [url for url in urls if 'federal-lobbying/industries/summary' in url]
    url_ids_df = pd.DataFrame(url_ids)
    ids = url_ids_df[0].str.split('id=')
    industry_id = []
    for i in range(len(ids)):
        industry_id.append(ids[i][1])
    return industry_id

# class ProPublica():
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.url = self.url + api_key
#     def senate_members(self):
#         headers = {'X-API-Key': self.api_key}
#         r = requests.get('https://api.propublica.org/congress/v1/117/senate/members.json', headers = headers)
#         propublica = r.json()
#         propublica_df = pd.DataFrame(propublica['results'][0]['members'])
#         senators_crp_id = propublica_df[propublica_df['in_office'] == True]
#         return senators_crp_id

# class OpenSecrets():
#     def __init__(self, api_key):
#         self.api_key = api_key
#     def state_senator_industry(self, state, industry):
#         self.api_key

# def top_senators_industry(industry):