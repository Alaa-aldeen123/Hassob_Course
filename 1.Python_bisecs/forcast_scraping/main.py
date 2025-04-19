from bs4 import BeautifulSoup
import requests
import re
from datetime import date
from tabulate import tabulate
import json



#get forcast data
def get_forcast_data():
    url= 'https://world-weather.info/'
    headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
              'cookie':'celsius=1'}
    response= requests.get(url,headers=headers)

    if response.ok:
        soup= BeautifulSoup(response.content,'html.parser')
        resorts= soup.find('div',id="resorts")

        #get cities
        re_cities= r'">([\w\s]+)<\/a><span>'
        cities= re.findall(re_cities,str(resorts))


        #get temps
        re_temps= r'<span>(\+\d+|-\d+)<span'
        temps= re.findall(re_temps,str(resorts))
        temps= [int(temp) for temp in temps]


        #get weather condition
        conditions_tags= resorts.find_all('span',class_='tooltip')
        conditions= [condition.get('title') for condition in conditions_tags]

        #cobine all variables
        data= zip(cities,temps,conditions)
        #data= list(data)
        return data

    return False

def get_forcast_text():
    data= get_forcast_data()

    if data:
        today= date.today().strftime('%d/%m/%Y')
        with open('output.txt','w',encoding='utf-8') as f:
            f.write("Popular Cities' Forcast" + '\n')
            f.write(today + '\n')
            f.write('='*30+'\n')
            table= tabulate(data, headers=['Cities','Temperature','Condition'],tablefmt='fancy_grid')
            f.write(table)

def get_forcast_json():
    data= get_forcast_data()

    if data:
        #title= "Popular Cities' Forcast"
        today= date.today().strftime('%d/%m/%Y')
        cities= [{'city':city,'temp':temp,'Condition': condition} for city,temp,condition in data]
        data_json= {'title':"Popular Cities' Forcast", 'date':today, 'Cities':cities}
        with open('output.json','w',encoding='utf-8') as f:
            json.dump(data_json,f,ensure_ascii=False)


if __name__=='__main__':
    get_forcast_text()
    get_forcast_json()