import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

df_dict = {
    'title':[], 
    'id':[],
    'authors':[],
    'abstract':[],
    'journal':[],
    'published':[]
}

df_arxiv = pd.DataFrame(df_dict)

# Base url = http://export.arxiv.org/api/
# method_name = query
# Here this is actual Base_url + method + ?

base_url = 'http://export.arxiv.org/api/query?'
search_query = ''
id_list = ''
start = 0
max_results = 10
sortBy = 'relevance'
sortOrder = 'ascending'

def url_to_scrape(base_url='http://export.arxiv.org/api/query?',search_query = '',id_list = '',start = 0,max_results = 10,sortBy = 'relevance',sortOrder = 'ascending'):
    url = base_url+'search_query='+search_query+'&'+'id_list='+id_list+'&'+'start='+str(start)+'&'+'max_results='+str(max_results)+'&'+'sortBy='+sortBy+'&'+'sortOrder='+sortOrder
    return url

def scraping_arxiv(total_papers = 10000, max_results=2000, search_query = 'all:physics'):
    for i in list(range(0, total_papers, max_results)):
        start = i
        res = requests.get(url_to_scrape(start = start,max_results = max_results, search_query = search_query))
        if (res.status_code == 200):
            soup = BeautifulSoup(res.content, 'lxml')
            yield soup
        else:
            print('Have an error:', res.status_code)

def paper_info(paper_details):
    title = paper_details.find('title').text
    urlid = paper_details.find('id').text
    published = pd.to_datetime(paper_details.find('published').text)
    abstract = paper_details.find('summary').text
    authors = [authors.find('name').text for authors in paper_details.find_all('author')]
    try:
        journal = paper_details.find('arxiv:journal_ref').text
    except:
        journal = 'None'
    dict_row = {
        'title':title, 
        'urlid':urlid,
        'published':published,
        'abstract':abstract,
        'authors':authors,
        'journal':journal
    }
    return dict_row

def create_dict(obj, df_dict):
    count=0
    for paper in obj.find_all('entry'):
        count+=1
        dummy_dict = paper_info(paper)
        df_dict['title'].append(dummy_dict['title'])
        df_dict['id'].append(dummy_dict['urlid'])
        df_dict['abstract'].append(dummy_dict['abstract'])
        df_dict['authors'].append(dummy_dict['authors'])
        df_dict['journal'].append(dummy_dict['journal'])
        df_dict['published'].append(dummy_dict['published'])
    print('papers added on this scrape: ',count)
    return df_dict

for obj in scraping_arxiv(total_papers=30000, max_results=2000, search_query='all:particle'):
    create_dict(obj, df_dict)
    time.sleep(3)

df_arxiv = pd.DataFrame(df_dict)

df_arxiv.drop_duplicates(subset='title', inplace=True)

df_arxiv.to_csv('./../arxiv_data/arxiv_particle_30000.csv', index = False)

print("\n ************* Exiting the arXiv scraping API code! ************************** \n")
