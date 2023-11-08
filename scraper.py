import requests
from bs4 import BeautifulSoup
import csv

# Base URL of IQAir website
url = 'https://www.iqair.com/id/indonesia/central-java/salatiga'

response = requests.get(url)

# Check if the request was successful (status code 200)
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

    # Write the extracted data to a CSV file
    with open('airQualityData.csv', mode='w') as csv_file:
        fieldnames = ['city', 'index', 'wind_dir', 'wind', 'pressure', 'time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        try:
            writer.writeheader()
            writer.writerow({'index': index, 'city': city.string, 'wind_dir': wind_dir, 'wind': wind, 'pressure': pressure, 'time': time})
        except:
            print("Error writing to CSV file.")

else:
    print('Failed to retrieve the webpage.')

