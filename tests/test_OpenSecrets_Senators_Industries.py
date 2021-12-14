from OpenSecrets_Senators_Industries import OpenSecrets_Senators_Industries
import pandas as pd
import os
from dotenv import load_dotenv

def test_top_20_industries_ids():
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
            'IDs': ['H04','F09', 'E01', 'E08', 'B12', 'N15', 'B09', 'W04', 'F07', 'N00', 'H02', 'W03', 'M01', 'H01',
                    'H03', 'D01', 'B02', 'F10', 'M02', 'F03']}
    expected = pd.DataFrame(data = data)
    result = OpenSecrets_Senators_Industries.top_20_industries_ids(year=2011)
    pd.testing.assert_frame_equal(result, expected)

def test_senate_members_head():
    load_dotenv()
    ProPublica = OpenSecrets_Senators_Industries.ProPublicaAPIKey(os.getenv('PROPUBLICA_KEY'))
    result = ProPublica.senate_members(117)[:10]
    data = {'first_name': ['Tammy', 'John', 'Michael', 'Marsha', 'Richard', 'Roy', 'Cory', 'John', 'Mike', 'Sherrod'],
            'middle_name': [None, None, None, None, None, None, None, None, None, None],
            'last_name': ['Baldwin', 'Barrasso', 'Bennet', 'Blackburn', 'Blumenthal', 'Blunt', 'Booker', 'Boozman',
                          'Braun', 'Brown'],
            'state': ['WI', 'WY', 'CO', 'TN', 'CT', 'MO', 'NJ', 'AR', 'IN', 'OH'],
            'crp_id': ['N00004367', 'N00006236', 'N00030608', 'N00003105', 'N00031685', 'N00005195', 'N00035267',
                       'N00013873', 'N00041731', 'N00003535']
            }
    expected = pd.DataFrame(data = data)
    pd.testing.assert_frame_equal(result, expected)

def test_senate_members_tail():
    load_dotenv()
    ProPublica = OpenSecrets_Senators_Industries.ProPublicaAPIKey(os.getenv('PROPUBLICA_KEY'))
    result = ProPublica.senate_members(117)[:]
    data = {'first_name': ['Tammy', 'John', 'Michael', 'Marsha', 'Richard', 'Roy', 'Cory', 'John', 'Mike', 'Sherrod'],
            'middle_name': [None, None, None, None, None, None, None, None, None, None],
            'last_name': ['Baldwin', 'Barrasso', 'Bennet', 'Blackburn', 'Blumenthal', 'Blunt', 'Booker', 'Boozman',
                          'Braun', 'Brown'],
            'state': ['WI', 'WY', 'CO', 'TN', 'CT', 'MO', 'NJ', 'AR', 'IN', 'OH'],
            'crp_id': ['N00004367', 'N00006236', 'N00030608', 'N00003105', 'N00031685', 'N00005195', 'N00035267',
                       'N00013873', 'N00041731', 'N00003535']
            }
    expected = pd.DataFrame(data = data)
    pd.testing.assert_frame_equal(result, expected)