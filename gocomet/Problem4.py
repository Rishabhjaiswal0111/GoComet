from bs4 import BeautifulSoup
import requests
import random
from tqdm import tqdm
import time
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
search=input("Enter product to campare ")
params_amaz= (
    ('k', search),
    ('ref', 'nb_sb_noss_2'),
)
params_flip = (
    ('q', search),
    ('otracker', 'search'),
    ('otracker1', 'search'),
    ('marketplace', 'FLIPKART'),
    ('as-show', 'on'),
    ('as', 'off'),
)
# response_amaz = requests.get('https://www.amazon.in/s', headers=headers, params=params_amaz)
response_flip = requests.get('https://www.flipkart.com/search', headers=headers, params=params_flip)
print(response_flip.status_code)

content=BeautifulSoup(response_flip.content,"html.parser")

all_link=[]
if content.find_all("a",{"class":"_1fQZEK"})!=[]:
        all_link=content.find_all("a",{"class":"_1fQZEK"})
elif content.find_all("a",{"class":"_2UzuFa"})!=[]:
        all_link=content.find_all("a",{"class":"_2UzuFa"})
else:
        all_link=content.find_all("a",{"class":"_2rpwqI"})

all_link=["https://www.flipkart.com"+i['href'] for i in all_link]

# all_link=content.find_all("a",{"class":"a-link-normal a-text-normal"})
# print(all_link)
# print(len(all_link))
# all_link=["https://www.amazon.in/"+i['href'] for i in all_link]
# for i in all_link:
#     print(i)
# print(len(all_link))
all_flip_data=[]
for link in tqdm(all_link[:5]):
    time.sleep(0.2)
    data = BeautifulSoup(requests.get(link).content, "html.parser")

    title=data.find_all("span", {"class": "B_NuCI"})[0].text
    price=data.find_all("div",{"class":"_30jeq3 _16Jk6d"})[0].text.replace("₹","")
    rate=data.find_all("div", {"class": "_3LWZlK"})[0].text

    model_no="NA"
    try:
        model_type=data.find_all("td",{"class":"_1hKmbr col col-3-12"})[1].text
        if model_type=="Model Number":
            model_no = data.find_all("li", {"class": "_21lJbe"})[1].text
    except:
        pass
    finally:
        all_flip_data.append([title,float(price.replace(",",'')),rate,link.split("&")[0],model_no,"Flipkart"])

fields = ['Title', 'Price', 'Rating','Link', 'Model_No','Source']
import pandas as pd
df=pd.DataFrame(all_flip_data[:5],columns=fields)
for i in tqdm(df['Model_No']):
    if i!="NA":
        params_amaz = (
            ('k', i.strip()),
            ('ref', 'nb_sb_noss_2'),
        )
        # print("current ---i----",i)
        response_amaz = requests.get('https://www.amazon.in/s', headers=headers, params=params_amaz)
        # print(response_amaz)
        data = BeautifulSoup(response_amaz.content, "html.parser")
        all_link_amaz = data.find_all("a", {"class": "a-link-normal a-text-normal"})
        all_link_amaz= ["https://www.amazon.in/" + j['href'] for j in all_link_amaz]
        all_link_amaz = [k.split("&")[0] for k in all_link_amaz]
        # print(all_link_amaz)
        if all_link_amaz!=[]:
            for j in all_link_amaz[:5]:
                # print(" --j ",j)
                model_data = BeautifulSoup(requests.get(j,headers=headers).content, "html.parser")
                # print(model_data)
                try:
                    model_no1=model_data.find_all("td",{"class":"a-size-base prodDetAttrValue"})[4].text
                    model_no2= model_data.find_all("td", {"class": "a-size-base prodDetAttrValue"})[3].text
                    # print(model_no1.strip(),"---m1")
                    # print(model_no2.strip(),"---bhai")
                except:
                    # print("--continue")
                    continue
                # print("i in model_no1",i.lower() in model_no1.lower())
                # print("i in model_no1", i.lower() in model_no2.lower())
                # print("i in model_no1", model_no1.lower() in i.lower())
                # print("i in model_no1", model_no2.lower() in i.lower())
                if i in model_no1 or i in model_no2 or model_no1 in i or model_no2 in i:
                        price = model_data.find_all("span", {"id": "priceblock_ourprice"})[0].text.replace("₹","").strip()
                        rate = model_data.find_all("span", {"class": "a-icon-alt"})[0].text.split(" ")[0]
                        # print("  PRICE---",price,rate)
                        # print(df.loc[df.Model_No==i,'Price'])
                        if float(df.loc[df.Model_No==i,'Price'])> float(price.replace(",",'')):
                            df.loc[df.Model_No == i, 'Price']=price
                            df.loc[df.Model_No == i, 'Rating'] = rate
                            df.loc[df.Model_No == i, 'Source'] = "AMAZON"
                            df.loc[df.Model_No == i, 'Link'] = j
                        else:
                            df.loc[df.Model_No == i, 'Title'] = df.loc[df.Model_No == i, 'Title']
                        break

    # print("---end---")
#
# print(df["Title"])
df2=df
df2['Title'] = '=HYPERLINK("' + df2['Link'] + '","'+df2['Title']+'")'
df2=df2.drop(['Link'],axis=1)

df2.to_excel(search+'.xlsx', index=True)