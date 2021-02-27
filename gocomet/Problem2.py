from bs4 import BeautifulSoup
import requests
import random

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
search=input("Search:- \n")
page_no='1'
number_of_product=input("\nEnter Number of product \n")
if number_of_product=='' or int(number_of_product)<10 :
    number_of_product='10'
    print("Default selected")
elif int(number_of_product)>50:
    number_of_product='50'
    print("Default selected\n")
sort_by=input(" Price \n1. low to high\n2. high to low\n3. relevance/featured\n4. new arrivals\n")
if sort_by=='' or int(sort_by)==3:
    sort_by='relevance'
    print("Default selected")
elif int(sort_by)==1:
    sort_by='price_asc'
elif int(sort_by)==2:
    sort_by='price_desc'
elif int(sort_by)==4:
    sort_by='recency_desc'

# print(number_of_product,sort_by)
print("\nEnter Price Range")
min_range=input("Min Range \n")
if min_range=='':
    min_range='Min'
    print("Default Min")
max_range=input("Max Range \n")
if max_range=='':
    max_range='Max'
    print("Default Max\n")


# params = (
#     ('q', search),
#     ('otracker', 'search'),
#     ('otracker1', 'search'),
#     ('marketplace', 'FLIPKART'),
#     ('as-show', 'on'),
#     ('as', 'off'),
#     ('sort', sort_by),
#     ('p%5B%5D','facets.price_range.from%3DMin'),
#     ('p%5B%5D','facets.price_range.to%3D40000'),
#     ('page', page_no),
# )
# params = {
#     'q': search,
#     'otracker':'search',
#     'otracker1': 'search',
#     'marketplace': 'FLIPKART',
#     'as-show': 'on',
#     'as': 'off',
#     'sort': sort_by,
#     'p': ['facets.price_range.from%3DMin', 'facets.price_range.to%3D40000'],
#     'page': page_no,
# }
# print(min_range,max_range)


# proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
# proxy=random.choice(proxies)



count=0
all_link_data=[]
while(count<=int(number_of_product)):
    # print(proxy)
    url="https://www.flipkart.com/search?q="+search+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort="+sort_by+"&p%5B%5D=facets.price_range.from%3D"+min_range+"&p%5B%5D=facets.price_range.to%3D"+max_range+"&page="+page_no
    response = requests.get(url, headers=headers)
    # response = requests.get(url, headers=headers,
    #                         proxies={"http": '117.212.90.231:41225', "https": '117.212.90.231:41225'})
    print(response)
    content=BeautifulSoup(response.content,"html.parser")
    if content.find_all("a",{"class":"_1fQZEK"})!=[]:
        all_link=content.find_all("a",{"class":"_1fQZEK"})
    elif content.find_all("a",{"class":"_2UzuFa"})!=[]:
        all_link=content.find_all("a",{"class":"_2UzuFa"})
    else:
        all_link=content.find_all("a",{"class":"_2rpwqI"})

    all_link=["https://www.flipkart.com"+i['href'] for i in all_link]
    page_no=str(int(page_no)+1)
    count=count+len(all_link)
    all_link_data.extend(all_link)
    # print(count,len(all_link_data),len(all_link),number_of_product,page_no)

for i in all_link_data[:int(number_of_product)]:
    print(i)



