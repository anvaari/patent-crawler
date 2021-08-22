"""
You should do this steps in order ro run this code:
    * Use Search_Url_Finder.py to Download CSV file which contain url of each patent
    * Copy it (CSV file) to path where this code exist
    * Rename it to gp-search.csv
    
This code extract this information from patents page from Google Patents and store them into datafram:
    - ID
    - Title
    - Abstract
    - Description
    - Claims
    - Inventors
    - Patent Office
    - Publication Date
    - URL
    
The code have capability to resume from last run. So don't worry if something unwanted happend (i.e  Power outage!)

This code create two files in the code directory :
    patents_data.csv --> Contain all information scraped from patents pages
    not_scrap_pickle --> Contain all pantents from gp-search.csv which weren't scrapped 
    
@author: zil.ink/anvaari
"""

# Import required packages
import pandas as pd
import requests
import progressbar
import time
import os
from os.path import join
from bs4 import BeautifulSoup
import pickle

script_path=os.path.dirname(os.path.abspath(__file__))

# Make sure gp-search.csv exist  
while not os.path.isfile(join(script_path,'gp-search.csv')):
    print('\nYou should do this steps in order ro run this code:\n\t* Use Search_Url_Finder.py to Download CSV file which contain url of each patent\n\t* Copy it (CSV file) to path where this code exist\n\t* Rename it to gp-search.csv\n')
    print("\ngp-search.csv doesn't find. It should exist where this code exist\n")
    temp_=input('\nPlease copy the file and  press Enter\n')
# Import search-gp.csv as dataframe
search_df=pd.read_csv(join(script_path,'gp-search.csv'),skiprows=[0])

# This piece add resume capability to code
# Load result (if exist) from code path and slice search-gp.csv from where last index of result to the end
if os.path.isfile(join(script_path,'patents_data.csv')):
    result=pd.read_csv(join(script_path,'patents_data.csv'),index_col=0)
    search_df=search_df.loc[result.index[-1]+1:,:]
else:
    result=pd.DataFrame(columns=['ID','Title','Abstract','Description','Claims','Inventors','Current Assignee','Patent Office','Publication Date','URL'])
# Load list of not scraped links if exist
if os.path.isfile(join(script_path,'not_scrap_pickle')):
    with open(join(script_path,'not_scrap_pickle'),'rb') as fp:
        not_scraped=pickle.load(fp)
else:
    not_scraped=[]

# Set user agent for every request send to google    
h={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}

# Iteate over search-gp.csv and send request to server
for (index,row),i in zip(search_df.iterrows(),progressbar.progressbar(range(len(search_df)))):
    link=row['result link']
    # Send request to Google Patents and scrap source of patent page
    # try except use in order handle connection errors
    try:
        r=requests.get(link,headers=h)
    except requests.exceptions.ConnectionError as e:
        not_scraped.append(link)
        print(e,'\n\n')
        # This piece closes the program if rate of errors go higher than 20% 
        if len(not_scraped)/int(index) >=0.2:
            print('\nAbove half of request result in erroe please read the output to investigate why this happend\n')
            break
        continue
    # Use Beautidulsoup to extract information from html
    bs=BeautifulSoup(r.content,'html.parser')
    # Find claims section
    claims=bs.find('section',{'itemprop':'claims'})
    # Handle situation where claims not exist
    if not claims is None:
        # Handle situation where claims have non-english paragraphs
        if claims.find('span',class_='notranslate') is None:
            claims=claims.text.strip()    
        else:
            notranslate=[tag.find(class_='google-src-text') for tag in  claims.find_all('span',class_='notranslate')]
            for tag in notranslate:
                tag.extract()
            claims=claims.text.strip()
            
    else: 
        claims='Not Found'
        
    desc=bs.find('section',{'itemprop':'description'})
    # Handle situation where description not exist
    if not desc is None:
        # Handle situation where description have non-english paragraphs
        if desc.find('span',class_='notranslate') is None:
            desc=desc.text.strip()
        else:
            notranslate=[tag.find(class_='google-src-text') for tag in  desc.find_all('span',class_='notranslate')]
            for tag in notranslate:
                tag.extract()
            desc=desc.text.strip()
    else:
        desc='Not Found'
        
    abst=bs.find('section',{'itemprop':'abstract'})
    # Handle situation where abstract not exist
    if not abst is None:
        # Handle situation where abstract have non-english paragraphs
        if abst.find('span',class_='notranslate') is None:
            abst=abst.text.strip()
        else:
            notranslate=[tag.find(class_='google-src-text') for tag in  abst.find_all('span',class_='notranslate')]
            for tag in notranslate:
                tag.extract()
            abst=abst.text.strip()
    else:
        abst='Not Found'
      
    
    patent_office=bs.find('dd',{'itemprop':'countryName'})
    # Handle situation where patent office name not exist
    if patent_office is None:
        patent_office='Not Found'
    else:
        patent_office=patent_office.text
    # Add information to result dataframe
    result.at[index,'ID']=search_df.at[index,'id']
    result.at[index,'Title']=search_df.at[index,'title']
    result.at[index,'Abstract']=abst
    result.at[index,'Description']=desc
    result.at[index,'Claims']=claims
    result.at[index,'Inventors']=search_df.at[index,'inventor/author']
    result.at[index,'Current Assignee']=search_df.at[index,'assignee']
    result.at[index,'Publication Date']=search_df.at[index,'publication date']
    result.at[index,'Patent Office']=patent_office
    result.at[index,'URL']=search_df.at[index,'result link']
    
    # Save result dataframe and not scraped list every 5 iteration
    if i%5==0:
        result.to_csv(join(script_path,'patents_data.csv'))
        with open(join(script_path,'not_scrap_pickle'),'wb') as fp:
            pickle.dump(not_scraped, fp)
    # Wain 70 seconds every 10 iteration in order to avoid blocking from google
    if i%10==0 and i!=0:
        time.sleep(70)
    
result.to_csv(join(script_path,'patents_data.csv'))
with open(join(script_path,'not_scrap_pickle'),'wb') as fp:
            pickle.dump(not_scraped, fp)
  
