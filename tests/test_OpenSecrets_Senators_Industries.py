from OpenSecrets_Senators_Industries import OpenSecrets_Senators_Industries
import pandas as pd
import os
from dotenv import load_dotenv
import pytest
from unittest.mock import patch


def test_top_20_industries_ids():
    result = OpenSecrets_Senators_Industries.top_20_industries_ids(year=2011)
    data = {'Industry': ['Pharmaceuticals/Health Products', 'Insurance', 'Oil & Gas', 'Electric Utilities',
                         'Electronics Mfg & Equip', 'Misc Manufacturing & Distributing', 'Telecom Services',
                         'Education', 'Securities & Investment', 'Business Associations', 'Hospitals/Nursing Homes',
                         'Civil Servants/Public Officials', 'Air Transport', 'Health Professionals',
                         'Health Services/HMOs', 'Defense Aerospace', 'TV/Movies/Music', 'Real Estate', 'Automotive',
                         'Commercial Banks'],
            'Total': ['$243,393,507', '$162,765,005', '$151,273,177', '$147,071,215', '$133,307,754', '$113,710,479',
                      '$106,361,985', '$106,266,831', '$105,552,226', '$105,477,318', '$100,243,890', '$93,981,205',
                      '$80,948,141', '$80,247,907', '$75,101,128', '$72,447,900', '$66,982,092', '$66,357,632',
                      '$62,871,705', '$61,584,654'],
            'IDs': ['H04', 'F09', 'E01', 'E08', 'B12', 'N15', 'B09', 'W04', 'F07', 'N00', 'H02', 'W03', 'M01', 'H01',
                    'H03', 'D01', 'B02', 'F10', 'M02', 'F03']}
    expected = pd.DataFrame(data=data)
    pd.testing.assert_frame_equal(result, expected)


@pytest.fixture
def senate_members_df():
    load_dotenv()
    ProPublica = OpenSecrets_Senators_Industries.ProPublicaAPIKey(os.getenv('PROPUBLICA_KEY'))
    df = ProPublica.senate_members()
    return df

def test_senate_members_head(senate_members_df):
    result = senate_members_df[:10]
    data = {'first_name': ['Tammy', 'John', 'Michael', 'Marsha', 'Richard', 'Roy', 'Cory', 'John', 'Mike', 'Sherrod'],
            'middle_name': [None, None, None, None, None, None, None, None, None, None],
            'last_name': ['Baldwin', 'Barrasso', 'Bennet', 'Blackburn', 'Blumenthal', 'Blunt', 'Booker', 'Boozman',
                          'Braun', 'Brown'],
            'state': ['WI', 'WY', 'CO', 'TN', 'CT', 'MO', 'NJ', 'AR', 'IN', 'OH'],
            'crp_id': ['N00004367', 'N00006236', 'N00030608', 'N00003105', 'N00031685', 'N00005195', 'N00035267',
                       'N00013873', 'N00041731', 'N00003535']
            }
    expected = pd.DataFrame(data=data)
    pd.testing.assert_frame_equal(result, expected)

def test_senate_members_tail(senate_members_df):
    result = senate_members_df[-10:]
    data = {None: [92, 93, 94, 95, 96, 97, 98, 99, 100, 101],
            'first_name': ['Patrick', 'Tommy', 'Chris', 'Mark', 'Raphael', 'Elizabeth', 'Sheldon', 'Roger', 'Ron',
                           'Todd'],
            'middle_name': ['J.', None, None, None, None, None, None, None, None, None],
            'last_name': ['Toomey', 'Tuberville', 'Van Hollen', 'Warner', 'Warnock', 'Warren', 'Whitehouse', 'Wicker',
                          'Wyden', 'Young'],
            'state': ['PA', 'AL', 'MD', 'VA', 'GA', 'MA', 'RI', 'MS', 'OR', 'IN'],
            'crp_id': ['N00001489', None, 'N00013820', 'N00002097', None, 'N00033492', 'N00027533', 'N00003280',
                       'N00007724', 'N00030670']
            }
    df = pd.DataFrame(data=data)
    expected = df.set_index(None)
    pd.testing.assert_frame_equal(result, expected)

@patch('builtins.print')
def test_senate_members_wrong_API_key(mock_print):
    ProPublica = OpenSecrets_Senators_Industries.ProPublicaAPIKey('wrongkey')
    ProPublica.senate_members()
    mock_print.assert_called_with('Error: Unexpected content returned from API. Check if API Key is correct.')

def test_top_senators_each_industry():
    load_dotenv()
    ProPublica = OpenSecrets_Senators_Industries.ProPublicaAPIKey(os.getenv('PROPUBLICA_KEY'))
    OpenSecrets = OpenSecrets_Senators_Industries.OpenSecretsAPIKey(os.getenv('OPENSECRETS_KEY'))
    result = OpenSecrets.top_senators_each_industry(ProPublica, congress_sitting=116).iloc[[0, 10, 20], :]
    data = {None: [0, 10, 20],
            'cand_name': ['Casey, Bob', 'Manchin, Joe', 'Brown, Sherrod'],
            'cid': ['N00027503', 'N00032838', 'N00003535'],
            'cycle': ['2018', '2018', '2018'],
            'industry': ['Pharm/Health Prod', 'Pharm/Health Prod', 'Pharm/Health Prod'],
            'last_updated': ['06/10/19', '06/10/19', '06/10/19'],
            'party': ['D', 'D', 'D'],
            'state': ['Pennsylvania', 'West Virginia', 'Ohio'],
            'total': [542125.0, 153166.0, 101436.0]
            }
    df = pd.DataFrame(data=data)
    expected = df.set_index(None)
    pd.testing.assert_frame_equal(result, expected)


@patch('builtins.print')
def test_top_senators_each_industry_wrong_API_key(mock_print):
    load_dotenv()
    ProPublica = OpenSecrets_Senators_Industries.ProPublicaAPIKey(os.getenv('PROPUBLICA_KEY'))
    OpenSecrets = OpenSecrets_Senators_Industries.OpenSecretsAPIKey('wrongkey')
    OpenSecrets.top_senators_each_industry(ProPublica)
    mock_print.assert_called_with('Error: Unexpected content returned from API. Check if API Key is correct.')