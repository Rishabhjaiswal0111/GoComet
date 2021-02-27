from bs4 import BeautifulSoup
import requests
import csv
import time
from tqdm import tqdm
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^88^\\^, ^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}
search=input("Search:- ")       # taking input from user (can be anything but relevant)
params = (
    ('q', search),
    ('as', 'on'),
    ('as-show', 'on'),
    ('otracker', 'AS_Query_TrendingAutoSuggest_1_0_na_na_na'),
    ('otracker1', 'AS_Query_TrendingAutoSuggest_1_0_na_na_na'),
    ('as-pos', '1'),
    ('as-type', 'TRENDING'),
    ('suggestionId', 'mobiles'),
    ('requestId', '5a6a663c-5e0e-4988-bd3b-2a4de789e935'),
    ('as-backfill', 'on'),
)

# adding header so that default python header of request module to override it otherwise,
# flipkart will detect that it's a automated request and will return some useless javascript data

response = requests.get('https://www.flipkart.com/search', headers=headers, params=params)

print(response)
# print(response.text)
# parsing data from response of our request only based of html content
content=BeautifulSoup(response.content,"html.parser")

# all_link=content.find_all("a",{"class":"_1fQZEK"}) if content.find_all("a",{"class":"_1fQZEK"})!=[] else content.find_all("a",{"class":"_2UzuFa"})

# looking for <a href> from html content of response with help of class selector
# while searching for <a href> class, founded that there were 3 different class for it

if content.find_all("a",{"class":"_1fQZEK"})!=[]:
    all_link=content.find_all("a",{"class":"_1fQZEK"})
elif content.find_all("a",{"class":"_2UzuFa"})!=[]:
    all_link=content.find_all("a",{"class":"_2UzuFa"})
else:
    all_link=content.find_all("a",{"class":"_2rpwqI"})

# adding https://www.flipkart.com at start to the link found from <a href> because it only contained from /data/data/data
all_link=["https://www.flipkart.com"+i['href'] for i in all_link]
# removing useless data from the links
all_link=[i.split("&")[0] for i in all_link]

# looking for title,price,rate,category,deliver,model_type from the above links founded
all_data=[]
for link in tqdm(all_link):
    time.sleep(0.3)
    data = BeautifulSoup(requests.get(link).content, "html.parser")

    title=data.find_all("span", {"class": "B_NuCI"})[0].text
    price=data.find_all("div",{"class":"_30jeq3 _16Jk6d"})[0].text.replace("₹","")
    rate=data.find_all("div", {"class": "_3LWZlK"})[0].text
    category=data.find_all("a", {"class": "_2whKao"})[1].text

    deliver="NA"
    model_no="NA"
    try:
        deliver = data.find_all("span", {"class": "_1TPvTK"})[0].text
        model_type=data.find_all("td",{"class":"_1hKmbr col col-3-12"})[1].text
        if model_type=="Model Number":
            model_no = data.find_all("li", {"class": "_21lJbe"})[1].text
    except:
        pass
    finally:
        all_data.append([title,price,rate,link,category,model_no,deliver,"Flipkart"])

# print(all_data)
fields = ['Title', 'Price(in rupees)', 'Rating','Link', 'Category','Model No','Delivered In ','Source']



import pandas as pd
df=pd.DataFrame(all_data,columns=fields)

df['Title'] = '=HYPERLINK("' + df['Link'] + '","'+df['Title']+'")'
df=df.drop(['Link'],axis=1)

df.to_excel(search+'.xlsx', index=False)