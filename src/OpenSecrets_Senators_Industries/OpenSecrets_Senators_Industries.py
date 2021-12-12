import requests
import json
from json.decoder import JSONDecodeError
import lxml
import pandas as pd
from bs4 import BeautifulSoup


def top_20_industries():
    url = 'https://www.opensecrets.org/federal-lobbying/industries'
    html = requests.get(url)
    df = pd.read_html(html.text)
    return df[:19]


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


def senate_members(propublicaapikey, state):
    headers = {'X-API-Key': propublicaapikey}
    r = requests.get('https://api.propublica.org/congress/v1/117/senate/members.json', headers=headers)
    senate_members = r.json()
    senate_members_df = pd.DataFrame(senate_members['results'][0]['members'])
    senators_crp_id = senate_members_df[senate_members_df['in_office'] == True][senate_members_df['state'] == state]['crp_id']
    return senators_crp_id


def overall_func():
    propublicaapikey = input('Enter ProPublica API Key: ')
    opensecretsapikey = input('Enter OpenSecrets API Key: ')
    state = input("Which state's senators would you like information about? ")
    total_response_df = pd.DataFrame()
    senators_crp_id = senate_members(propublicaapikey, state)
    industry_id = top_20_industries_ids()
    for senator in senators_crp_id:
        for industry in industry_id:
            params = {'apikey': opensecretsapikey, 'cid': senator, 'ind': industry, 'output': 'json'}
            r_opensecrets = requests.get('https://www.opensecrets.org/api/?method=candIndByInd&', params=params)
            try:
                r_json = r_opensecrets.json()
                r_df = pd.DataFrame(r_json['response']['candIndus'])
                r_df_transpose = r_df.transpose()
                total_response_df = pd.concat([total_response_df, r_df_transpose])
            except JSONDecodeError:
                pass
    return total_response_df

# class ProPublicaAPIKey:
#     def __init__(self, api_key):
#         self.api_key = api_key
#
#     def senate_members(self):
#         headers = {'X-API-Key': self.api_key}
#         r = requests.get('https://api.propublica.org/congress/v1/117/senate/members.json', headers = headers)
#         senate_members = r.json()
#         senate_members_df = pd.DataFrame(senate_members['results'][0]['members'])
#         senators_crp_id = senate_members_df[senate_members_df_df['in_office'] == True]
#         return senators_crp_id


# class OpenSecretsAPIKey:
#     def __init__(self, api_key):
#         self.api_key = api_key
#
#     def overall_funct(self):
#         for senator in senators_crp_id:
#             for industry in industry_id:
#                 params = {'apikey': os.getenv('OPENSECRETS_KEY'), 'cid': senator, 'ind': industry, 'output': 'json'}
#                 r_opensecrets = requests.get('https://www.opensecrets.org/api/?method=candIndByInd&', params=params)
#                 try:
#                     r_json = r_opensecrets.json()
#                     r_df = pd.DataFrame(r_json['response']['candIndus'])
#                     r_df_transpose = r_df.transpose()
#                     total_response_df = pd.concat([total_response_df, r_df_transpose])
#                 except JSONDecodeError:
#                     pass
