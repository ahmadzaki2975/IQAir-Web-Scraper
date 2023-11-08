import requests
from bs4 import BeautifulSoup
import csv

# list endpoints to scrape
endpoints = [
    '/jakarta',
    '/yogyakarta',
    '/west-java/bandung',
    '/central-java/salatiga',
    '/central-java/semarang',
    '/central-java/surakarta',
]

# Base URL of IQAir website
url = 'https://www.iqair.com/id/indonesia'
dataBuffer = []

def scrape(endpoint) :
    response = requests.get(url + endpoint)
    print("Scraping " + url + endpoint)
    # Check if the request was successful (status code 200)
    try:
        if response.status_code == 200:
        # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
        
            title = soup.find('h1', class_='pagetitle__title').contents[0]
            index = soup.find('p', class_='aqi-value__value').contents[0]
            city = soup.find('a', class_="breadcrumb__item is-active")
            table_element = soup.find('table', attrs={'_ngcontent-airvisual-web-c224': ""})
            wind = "0 km/h"
            pressure = "0 mbar"
            for td in table_element.find_all('td'):
                if ("mbar" in td.text):
                    pressure = td.text
                if ("km/h" in td.text):
                    wind = td.text
            time = soup.find('time').string.strip()
            icon_parent = soup.find('img', class_="forecast-wind_icon")
            wind_dir = icon_parent.get('alt')
            
            # Print the extracted data
            print("=====================================")
            print('Title:', title)
            print('Index:', index)
            print('City:', city.string)
            print('Wind Direction:', wind_dir)
            print('Wind Speed:', wind)
            print('Wind Pressure:', pressure)
            print('Last Update:', time)
            print("=====================================")

            # append to buffer
            dataBuffer.append({
                'city': city.string,
                'index': index,
                'wind_dir': wind_dir,
                'wind_spd': wind,
                'pressure': pressure,
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
    fieldnames = ['city', 'index', 'wind_dir', 'wind_spd', 'pressure', 'last_update']
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