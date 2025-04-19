from bs4 import BeautifulSoup
import requests
import csv


def get_data():
    url = 'https://www.accuweather.com/en/ye/yemen-weather'
    header = headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'}

    request = requests.get(url= url, headers=header)
    page = BeautifulSoup(request.content, 'html.parser')

    all_data = page.find('div',class_='nearby-locations-list')
    cities = all_data.find_all('span',class_='text title no-wrap')
    temps = all_data.find_all('span',class_='text temp')

    return zip(cities, temps)

def create_csv():
    if get_data():

        with open('output.csv', mode='w', newline='') as file:
            writer = csv.writer(file)


            writer.writerow(['city', 'temperature'])


            for city_tag, temp_tag in get_data():
                city = city_tag.get_text(strip=True)
                temp = temp_tag.get_text(strip=True)
                writer.writerow([city, temp])

    else:
        return 'No data Available'


if __name__ == '__main__':
    get_data()
    create_csv()