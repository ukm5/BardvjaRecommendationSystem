#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from global_params import search_queries, path_to_arxiv_data, max_papers_to_be_scraped, max_papers_in_single_call
import sys

if not (os.path.isdir(f'{path_to_arxiv_data}')):
    print("Missing directory for data from arxiv")
    print(f"Creating a new directory path: {path_to_arxiv_data}")
    os.mkdir(f'{path_to_arxiv_data}')

print("Search queries obtained to perform arxiv search: ",search_queries)
    
def one_big_scraping_function(query):
    # Dictionary to contain the papers from arxiv
    # The dict is converted to a dataframe
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
    search_query = query
    id_list = ''
    start = 0
    max_results = 10
    sortBy = 'relevance'
    sortOrder = 'descending'

    # Create the exact url that is parsed to obtain papers
    def url_to_scrape(base_url='http://export.arxiv.org/api/query?',search_query = '',id_list = '',start = 0,max_results = 10,sortBy = 'relevance',sortOrder = 'ascending'):
        url = base_url+'search_query='+search_query+'&'+'id_list='+id_list+'&'+'start='+str(start)+'&'+'max_results='+str(max_results)+'&'+'sortBy='+sortBy+'&'+'sortOrder='+sortOrder
        return url

    # Parsing the page with paper info
    def scraping_arxiv(total_papers = max_papers_to_be_scraped, max_results=max_papers_in_single_call, search_query = 'all:physics+OR+mathematics+OR+biology+OR+statistics+OR+politics'):
        for i in list(range(0, total_papers, max_results)):
            start = i
            res = requests.get(url_to_scrape(start = start,max_results = max_results, search_query = search_query))
            if (res.status_code == 200):
                soup = BeautifulSoup(res.content, 'lxml')
                yield soup
            else:
                print(f'Have an error scraping for {search_query}:', res.status_code)

    # Extracting details to be stored in dict
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

    # Adding the info into a dict
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

    # Submitting request to scrape different pages
    for obj in scraping_arxiv(total_papers=max_papers_to_be_scraped, max_results=max_papers_in_single_call, search_query=f'all:{query}'):
        create_dict(obj, df_dict)
        time.sleep(3)

    # Creating a dataframe
    df_arxiv = pd.DataFrame(df_dict)

    # Dropping duplicates
    df_arxiv.drop_duplicates(subset='title', inplace=True)

    # Creating a csv file
    df_arxiv.to_csv(f'{path_to_arxiv_data}arxiv_{query}_{max_papers_to_be_scraped}.csv', index = False)
    

for query in search_queries:
    print(f"Starting scraping arXiv for papers under '{query}' ...")
    one_big_scraping_function(query)


# In[5]:


print("HeeeeeeeHAaaaaaaa!")


# In[ ]:




