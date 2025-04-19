import requests
from bs4 import BeautifulSoup

#get all page data
url='https://www.amazon.com/Fossil-JR1354-Stainless-Chronograph-Leather/dp/B0066T2GAQ/ref=sr_1_4?_encoding=UTF8&content-id=amzn1.sym.db94be39-53f1-4c79-89b2-88aa81be709e&dib=eyJ2IjoiMSJ9.ul0blFngX7H7UGsQtJlbw3I_eWL8rUiJIJ_QqAqIfF4raD1KBvdNH1393AgA8Rw1JY8I7lBvI7e-ZCwTIrWwKaVEiK6ozZxcL3Y86EIkAGjqWkyynesCA4YEtRKu-bsFXFoHEklI231doQdIlUCngAxjsDt7ZlwGTF5wLs6qcrTW4lgAWlcz_jYuGBt1aCcu0uaV1V-JPAPp90sKsG_mxRTZFQ0iPCSlrZ-LFlk9FyCxiIdzoJEOIfpwxUa2Hp9s8XceC36CZQwKv2NUg1XVLDI6LTKoYgCY7jf2SjSYVJjTqqYhFjxxPh2IexMkJEEnJPi7ysKGpeNW7BZAIMdE0suw7RubVa3YnqTzF_n3hKvi30fVF-QjwRv_hJsEtMyjyHiLhLhv9v5h4Ks8Pfa_M1j-8p73dMIAGUMWsPsN0pV1aYV3wdUSdOukLsXEqHdn.EIktGo-1k5mBrPMqxL8TWReQV6a635gZ5-XZjgipIjc&dib_tag=se&keywords=men+watches&pd_rd_r=bff4b9b3-2424-4005-8f58-36a63caa6be3&pd_rd_w=4uBxK&pd_rd_wg=Ip4sM&pf_rd_p=db94be39-53f1-4c79-89b2-88aa81be709e&pf_rd_r=AW6Y2D4PK942K7VG0M11&qid=1736875432&sr=8-4'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
          ,'Accept-Language': 'en-US,en;q=0.9'}
get_info = requests.get(url,headers=header,params={'k':'men+watches'})
soup = BeautifulSoup(get_info.content,'html.parser')

#get title
title = soup.find('span',id='productTitle')

#get price data
whole_price = soup.find('span',class_="a-size-mini olpMessageWrapper")
price_only= whole_price.find('br')

#get image data
img=soup.find('img',alt="Fossil Nate Men&#39;s Watch with Oversized Chronograph Watch Dial and Stainless Steel or Leather Band")

#get table data
table= soup.find('table',id="technicalSpecifications_section_1")
teq_details = {}
rows = table.find_all('tr')
for row in rows:
    key = row.th.string.strip()
    value = row.td.string.strip()
    teq_details[key]=value


#print all outcomes
print(title.string.strip())
#print(price_only.string)#string: get text but not include (nested tags ==>'None' result)  str
print(price_only.get_text())#get_text: extracts the text including nested tags  ==> method
print(img['src'])
print(teq_details)

