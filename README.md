# Patent Crawler 
Patent Crawler is a python program to crawl patent information from [Google Patent](https://patents.google.com/) with given keywords.

## How It Works?
Google set very low rate-limit on search pages and block any activity wich detect them as scraping. But don't have such policy on each patent page. So at first I download list of patent which include few information include URL, then go to URLs and scrap them.
**I tried to wrote these programs in user friendly way. So running program will guide you to scrap what ever you want.**


## Usage

- Clone the repo
- Create a virtual environment and activate it. [How](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
    - `pip install -r requirements.txt`
- Download gecko driver for **firefox** from [here](https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/#quick-reference) and place it into code path.
- Now it's time to download gp-search.csv, csv which contain all search result for your keyword. [Search_Url_Finder.py](https://github.com/anvaari/patent-crawler/blob/main/Search_Url_Finder.py) guide you step by step to download this csv Or you can do it manualy by go to [Google Patent](https://patents.google.com/).
    - `python Search_Url_Finder.py`
- Rename downloaded csv file to `gp-search.csv` and place it into code path.
- Now run [Patent_Crawler.py](https://github.com/anvaari/patent-crawler/blob/main/Patent_Crawler.py). It will scrap information of all patents in `gp-search.csv` and save them to `patents_data.csv`.
    - `python Patent_Crawler.py`


## Notes


- Patent_Crawler extract this information from patents page (Google Patents) and store them into datafram:
    - ID
    - Title
    - Abstract
    - Description
    - Claims
    - Inventors
    - Patent Office
    - Publication Date
    - URL
    
- Patent_Crawler have capability to resume from last run. So don't worry if something unwanted happend (i.e  Power outage!)
    - Patent_Crawler save data on hard drive after scrap every 5 patents. This can slow down proccess when data became very larg (when we have larg number of patents), So it's better to set this 15 or 30 for better speed.

- Google will block IP if number of requests exceed specific number in each hour (or overal, I don't know it). So I set some `sleep` in code. You can reduce time of sleep but it increase probability of getting banned! 

- Two files will create in the code directory :
    - patents_data.csv --> Contain all information scraped from patents pages
    - not_scrap_pickle --> Contain all pantents from gp-search.csv which haven't be scrapped 


## Contribution

I really love open source community. It makes me proud to be a part of this community. So feel free to send any pull request or question in issues.

Hope this Pantent_Crawler can help you :)