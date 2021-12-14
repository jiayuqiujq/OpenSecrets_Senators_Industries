from json.decoder import JSONDecodeError
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml

# Web-scrapping the OpenSecrets Website for the Top 20 Industries that have spent the most on Federal Lobbying
def top_20_industries_ids(year='a'):
    """
    Extracts the Top 20 Industries that have spent the most on Federal Lobbying from
    https://www.opensecrets.org/federal-lobbying/industries.

    Parameters
    ----------
    year : Specify a specific year (1998 - 2021) for which to retrieve the data. Default is set to include the total
    amount of money spent on Federal Lobbying across all years from 1998 - 2021.

    Returns
    -------
    pandas.DataFrame
        Pandas DataFrame containing the Top 20 Industries that have spent the most on Federal Lobbying, the amount of
        money they have each spent, and their unique Industry IDs.

    Examples
    --------
    >>> from OpenSecrets_Senators_Industries import OpenSecrets_Senators_Industries
    >>> top_20_industries_ids()
    [   Industry	Total	IDs
    0	Pharmaceuticals/Health Products	$4,990,257,367	H04
    1	Insurance	$3,210,878,113	F09
    2	Electronics Mfg & Equip	$2,795,736,767	B12
    3	Electric Utilities	$2,757,808,440	E08
    4	Business Associations	$2,623,983,096	N00
    5	Oil & Gas	$2,489,418,498	E01
    6	Hospitals/Nursing Homes	$2,025,651,797	H02
    7	Misc Manufacturing & Distributing	$2,008,839,171	N15
    8	Education	$1,902,258,320	W04
    9	Securities & Investment	$1,897,760,970	F07
    10	Civil Servants/Public Officials	$1,887,599,161	W03
    11	Telecom Services	$1,883,769,733	B09
    12	Real Estate	$1,874,450,800	F10
    13	Air Transport	$1,730,349,996	M01
    14	Health Professionals	$1,712,045,500	H01
    15	Health Services/HMOs	$1,405,134,830	H03
    16	Automotive	$1,322,462,732	M02
    17	TV/Movies/Music	$1,301,018,584	B02
    18	Misc Issues	$1,247,693,549	Q10
    19	Defense Aerospace	$1,232,991,613	D01     ]

    """
    url = ('https://www.opensecrets.org/federal-lobbying/industries?cycle=' + str(year))
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    # Extracting all the URLs from the website
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    # Extracting URLs that contain the unique industry IDs corresponding to each of the Top 20
    url_ids = [url for url in urls if 'federal-lobbying/industries/summary' in url]
    url_ids_df = pd.DataFrame(url_ids)
    # Splitting the IDs from the rest of the URL
    ids = url_ids_df[0].str.split('id=')
    # Extracting list of unique industry IDs corresponding to each industry
    industry_id = []
    for i in range(len(ids)):
        industry_id.append(ids[i][1])
    # Extracting table of Top 20 Industries that have spent the most on Federal Lobbying along with the respective 
    # amounts they have spent 
    df = pd.read_html(html.text)[0][:20]
    # Adding a column to the table which contains the industry IDs corresponding to each Industry
    df['IDs'] = industry_id
    return df


class ProPublicaAPIKey:
    def __init__(self, propublica_api_key):
        self.propublica_api_key = propublica_api_key

    def senate_members(self, congress_sitting=117):
        """
        Uses the ProPublica API to extract a list of Senators.

        Parameters
        ----------
        congress_sitting : Allows the user to specify senators from which sitting of Congress (80-117) they would like
        information about. Default is set as the 117th Congress.

        Returns
        -------
        pandas.DataFrame
            Pandas DataFrame containing the names, state and CRP IDs of all senators in a particular sitting of
            Congress.

        Examples
        --------
        >>> from OpenSecrets_Senators_Industries import OpenSecrets_Senators_Industries
        >>> ProPublica = ProPublicaAPIKey('insert ProPublica API Key here')
        >>> ProPublica.senate_members()
        [	first_name	middle_name	last_name	state	crp_id
        0	Tammy	None	Baldwin	WI	N00004367
        1	John	None	Barrasso	WY	N00006236
        2	Michael	None	Bennet	CO	N00030608
        3	Marsha	None	Blackburn	TN	N00003105
        4	Richard	None	Blumenthal	CT	N00031685
        ...	...	...	...	...	...
        97	Elizabeth	None	Warren	MA	N00033492
        98	Sheldon	None	Whitehouse	RI	N00027533
        99	Roger	None	Wicker	MS	N00003280
        100	Ron	None	Wyden	OR	N00007724
        101	Todd	None	Young	IN	N00030670
        102 rows × 5 columns    ]

        """
        headers = {'X-API-Key': self.propublica_api_key}
        r = requests.get('https://api.propublica.org/congress/v1/' + str(congress_sitting) + '/senate/members.json',
                         headers=headers)
        senate_members = r.json()
        senate_members_df = pd.DataFrame(senate_members['results'][0]['members'])
        new_cols = ['first_name', 'middle_name', 'last_name', 'state', 'crp_id']
        senators_crp_id = senate_members_df[new_cols]
        return senators_crp_id


class OpenSecretsAPIKey:
    def __init__(self, opensecrets_api_key):
        self.opensecrets_api_key = opensecrets_api_key

    def top_senators_each_industry(self, propublica_api_key, industry_id='H04', **kwargs):
        """
        Uses the OpenSecretsAPI and ProPublica API to provide the user with the senators who have received the most
        amount of funding from each industry.

        Note that as the function makes as many calls as there are senators in a particular sitting of Congress, the
        function may take a while to return the necessary results.

        Parameters
        ----------
        propublica_api_key: The user's ProPublica API Key, initialised in the following way: propublica_api_key =
        ProPublicaAPIKey('insert ProPublica API Key here')

        industry_id: Unique industry_id. Full list of industry IDs can be found at
        www.opensecrets.org/downloads/crp/CRP_IDs.xls. Alternatively, the user can also call
        top_20_industries_ids() to retrieve the industry_idss corresponding to the Top 20 Industries that have spent the
        most on lobbying in each year (1998 - 2021) or in total from 1998 - 2021. The default is set to 'H04',
        corresponding to the Pharmaceuticals/Health Products industry.

        Returns
        -------
        pandas.DataFrame
            Pandas DataFrame containing the names, state and CRP IDs of all senators in a particular sitting of
            Congress.

        Examples
        --------
        >>> from OpenSecrets_Senators_Industries import OpenSecrets_Senators_Industries
        >>> OpenSecrets = OpenSecretsAPIKey('insert OpenSecrets API Key here')
        >>> propublica_api_key = ProPublicaAPIKey('insert ProPublica API Key here')
        >>> OpenSecrets.top_senators_each_industry(propublica_api_key, industry_id = 'F09', congress_sitting = 116)
        [ 	cand_name	chamber	cid	cycle	indivs	industry	last_updated	origin	pacs	party	rank	source	state	total
@attributes	Casey, Bob	S	N00027503	2018	223570	Insurance	06/10/19	Center for Responsive Politics	134250	D	2	http://www.opensecrets.org/industries/recips.p...	Pennsylvania	357820.0
@attributes	Scott, Rick	S	N00043290	2018	287712	Insurance	06/10/19	Center for Responsive Politics	41200	R	5	http://www.opensecrets.org/industries/recips.p...	Florida	328912.0
@attributes	Brown, Sherrod	S	N00003535	2018	155718	Insurance	06/10/19	Center for Responsive Politics	161082	D	6	http://www.opensecrets.org/industries/recips.p...	Ohio	316800.0
@attributes	McSally, Martha	S	N00033982	2018	192825	Insurance	06/10/19	Center for Responsive Politics	102000	R	7	http://www.opensecrets.org/industries/recips.p...	Arizona	294825.0
@attributes	Stabenow, Debbie	S	N00004118	2018	130900	Insurance	06/10/19	Center for Responsive Politics	161500	D	8	http://www.opensecrets.org/industries/recips.p...	Michigan	292400.0
...	...	...	...	...	...	...	...	...	...	...	...	...	...	...
@attributes	Boozman, John	S	N00013873	2018	3450	Insurance	06/10/19	Center for Responsive Politics	0	R	105	http://www.opensecrets.org/industries/recips.p...	Arkansas	3450.0
@attributes	Lee, Mike	S	N00031696	2018	1250	Insurance	06/10/19	Center for Responsive Politics	2000	R	106	http://www.opensecrets.org/industries/recips.p...	Utah	3250.0
@attributes	Udall, Tom	S	N00006561	2018	1058	Insurance	06/10/19	Center for Responsive Politics	0	D	108	http://www.opensecrets.org/industries/recips.p...	New Mexico	1058.0
@attributes	Leahy, Patrick	S	N00009918	2018	15	Insurance	06/10/19	Center for Responsive Politics	1000	D	109	http://www.opensecrets.org/industries/recips.p...	Vermont	1015.0
@attributes	Shelby, Richard C	S	N00009920	2018	0	Insurance	06/10/19	Center for Responsive Politics	-5000	R	112	http://www.opensecrets.org/industries/recips.p...	Alabama	-5000.0     ]

        """
        senators_crp_id = propublica_api_key.senate_members(**kwargs)['crp_id']
        total_response_df = pd.DataFrame()
        for senator_id in senators_crp_id:
            params = {'apikey': self.opensecrets_api_key, 'cid': senator_id, 'ind': industry_id, 'output': 'json'}
            r_opensecrets = requests.get('https://www.opensecrets.org/api/?method=candIndByInd&', params=params)
            try:
                r_json = r_opensecrets.json()
                r_df = pd.DataFrame(r_json['response']['candIndus'])
                r_df_transpose = r_df.transpose()
                total_response_df = pd.concat([total_response_df, r_df_transpose])
            except JSONDecodeError:
                pass
        total_response_df['total'] = total_response_df['total'].astype(float)
        return total_response_df.sort_values('total', ascending=False)
