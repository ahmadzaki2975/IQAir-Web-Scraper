import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# list endpoints to scrape
endpoints = [
    '/jakarta',
    '/yogyakarta',
    '/yogyakarta/sleman',
    '/west-java/bandung',
    '/central-java/salatiga',
    '/central-java/semarang',
    '/central-java/surakarta',
    '/aceh/banda-aceh',
]

# Base URL of IQAir website
url = 'https://www.iqair.com/id/indonesia'
dataBuffer = []

def format_id(kota, date):
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    formatted_date = date_obj.isoformat()
    return kota + "_" + formatted_date

def scrape(endpoint, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    response = requests.get(url + endpoint)
    print("Scraping " + url + endpoint)
    # Check if the request was successful (status code 200)
    try:
        if response.status_code == 200:
        # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1', class_='pagetitle__title').contents[0]
            index = soup.find('p', class_='aqi-value__value').contents[0]
            city = soup.find('a', class_="breadcrumb__item is-active").get_text()
            city = city.replace("Kota ", "").replace("Kab. ", "")
            city = city.strip()
            table_element = soup.find('table', attrs={'_ngcontent-airvisual-web-c224': ""})
            wind = "0 km/h"
            pressure = "0 mbar"
            for td in table_element.find_all('td'):
                if ("mbar" in td.text):
                    pressure = td.text
                if ("km/h" in td.text):
                    wind = td.text
            icon_parent = soup.find('img', class_="forecast-wind_icon")
            wind_dir = icon_parent.get('alt')
            
            # Print the extracted data
            print("=====================================")
            print('Title:', title)
            print('Index:', index)
            print('City:', city)
            print('Wind Direction:', wind_dir)
            print('Wind Speed:', wind)
            print('Wind Pressure:', pressure)
            print('Last Update:', time)
            print("=====================================")

            # append to buffer
            dataBuffer.append({
                'id': format_id(city, time),
                'city': city,
                'iqa': index,
                'wind_dir(deg)': wind_dir,
                'wind_spd(km/h)': wind,
                'pressure(mbar)': pressure,
                'last_update': time
            })

        else:
            print('Failed to retrieve the webpage.')
            
    except:
        print('Error Occured.')

for endpoint in endpoints:
    scrape(endpoint)
    
# Write the extracted data to a CSV file
iter = 0
with open('airQualityData.csv', mode='w') as csv_file:
    fieldnames = ['id', 'city', 'iqa', 'wind_dir(deg)', 'wind_spd(km/h)', 'pressure(mbar)', 'last_update']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    try:
        writer.writeheader()
        for data in dataBuffer:
            writer.writerow(data)
            iter += 1
        print("Successfully wrote " + str(iter) + " rows to CSV file.")
    except csv.Error as e:
        print("Error writing to CSV file.")
        print(e)