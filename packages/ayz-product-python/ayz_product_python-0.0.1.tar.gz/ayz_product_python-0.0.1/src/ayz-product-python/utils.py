import requests
import pandas as pd
import pandas_gbq
import time

class CreatorIQAPI:

  def __init__(self, architecture, api_key, url):
    self.architecture = architecture
    self.api_key = api_key
    self.headers = {}
    self.headers['Content-Type'] = 'application/json'
    self.url = url
    if architecture == 'REST':
      self.headers = {'X-API-KEY': api_key}
    elif architecture == 'GraphQL':
      self.headers = {'Authorization': f'ciq_token {api_key}'}
    else:
      print("architecture must be 'REST' of 'GraphQL'")

  def get_response(self, url, json=None):
    if self.architecture == 'REST':
      response = requests.get(url=url, headers=self.headers, params=json)
    elif self.architecture == 'GraphQL':
      response = requests.post(url=url, headers=self.headers, json=json)
    if response.status_code != 200:
      print(f"Failed to fetch data: {response.status_code} {response.text}")
    else:
      response_dict = response.json()
      print('API call succeeded')
      if response_dict.get('errors') is not None:
        print(f"Error in fetched data: {response_dict['errors'][0]['message']}")
      else:
        print('No error detected in response')
    return response_dict

class CampaignDataFetcher:

  def __init__(self,api_client):
    self.api_client = api_client

  def fetch_campaigns(self,campaigns, fields, max_size):
    payload = {'fields': fields, 'size': max_size}
    all_data = []
    for campaign in campaigns:
      url = f"{self.api_client.url}/{campaign}/activity"
      response = self.api_client.get_response(url=url, json=payload)
      data = response.get("CampaignActivity", {}).get("items", [])
      print(f'Campaign {campaign} completed with {len(data)} records')
      all_data.extend(data)
    print('---')
    print('All campaigns completed')
    print('---')
    return all_data

class GQLDataFetcher:

  def __init__(self, api_client):
    self.api_client = api_client
    self.out = []
    self.counts = []
    self.iteration = 0
    self.end_cursor = ""
    self.has_next_page = True


  def process_response(self, json):
    url = self.api_client.url
    response = self.api_client.get_response(url=url,json=json)
    self.end_cursor = response['data']['getPosts']['pageInfo']['endCursor']
    self.has_next_page = response['data']['getPosts']['pageInfo']['hasNextPage']
    data = response['data']['getPosts']['edges']
    self.out.extend(data)
    self.counts.append(response['data']['getPosts']['totalCount'])
    self.iteration += 1
    print(f'Iteration {self.iteration} completed with {len(data)} records')


  def fetch_pages(self, query, wait_time, max_size):
    json = {'query': query}
    #first call
    self.process_response(json)
    #iterate through pages
    while self.has_next_page != False:
      time.sleep(wait_time) #for throttling
      json['variables'] = {"after": self.end_cursor, "first":max_size}
      self.process_response(json)
    print('---')
    print('All iterations completed')
    print('---')
    pagination_checker = PaginationChecker(actual_count=len(self.out),counts=self.counts)
    pagination_checker.check_count()
    data = [nd['node'] for nd in self.out]
    return data

class PaginationChecker:

  def __init__(self, actual_count, counts):
    self.actual_count = actual_count
    self.counts = counts

  def check_count(self):
    count_min, count_max = min(self.counts), max(self.counts)
    print(f'# records retrieved: {self.actual_count}')
    if count_min == count_max:
        print(f'# records expected: {count_min}')
        print('result: success' if count_max == self.actual_count else 'there was a problem')
    else:
        print('# records changed between the beginning and the end of the api calls')
        print(f'min # records: {count_min}')
        print(f'max # records: {count_max}')
        print('# records within range' if count_min <= self.actual_count <= count_max else 'there was a problem')

def expand_column(df, old_col, new_col, field):
  def expand_column_lambda(row, column, field):
    c = row[column]
    l = [d[field] for d in c] if c is not None else None
    return l
  df[new_col] = df.apply(lambda x: expand_column_lambda(x, old_col, field), axis=1)
  df = df.drop(columns=[old_col])
  return df

class TagDataProcessor:

  def __init__(self, gql_data):
    self.gql_data = gql_data

  def build_tag_df(self, new_col):
    df = pd.json_normalize(
      data=self.gql_data,
      record_path="campaigns",
      meta=["id","contentTags"],
      record_prefix="campaign_")
    df = expand_column(df=df, old_col='contentTags', new_col=new_col, field='name')
    df = df.astype({
    'campaign_id':int,
    'id':int,
    'tags': str #needed if not using REPEATED with schema
    })
    df.rename(columns={
        'campaign_id':'CampaignId',
        'id':'Id'
        }, inplace=True)
    df = df.replace('None',None)
    return df