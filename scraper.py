import random
import time
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import json
import sqlite3
import queue


def get_soup_with_retry(url):
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81']
    referer = ['https://www.flipkart.com',
               'https://www.flipkart.com/wearable-smart-devices/smart-watches/pr?sid=ajy%2Cbuh&marketplace=FLIPKART&hpid=SVKCw8G6nMCuH4Eqbt2Crap7_Hsxr70nj65vMAAFKlc%3D&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJGcm9tIOKCuTEsMzk5Il0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwiaGVyb1BpZCI6eyJzaW5nbGVWYWx1ZUF0dHJpYnV0ZSI6eyJrZXkiOiJoZXJvUGlkIiwiaW5mZXJlbmNlVHlwZSI6IlBJRCIsInZhbHVlIjoiU01XR040WUVXR05aMkdHTSIsInZhbHVlVHlwZSI6IlNJTkdMRV9WQUxVRUQifX0sInRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkZhc3RyYWNrIFNtYXJ0d2F0Y2hlcyJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D&sort=popularity&page=1',
               'https://www.flipkart.com/wearable-smart-devices']
    session = HTMLSession()
    ua = UserAgent()
    headers = {'User-Agent': random.choice(user_agents),
               'Referer': 'https://www.google.com',
               'Language': 'en-US',
               'Encoding': 'gzip, deflate, br',
               'DNT': '1',
               'Upgrade-Insecure-Requests': '1'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    if response.status_code != 200 or 'recaptcha' in soup.prettify():
        for i in range(3):
            print(f"Response not 200. Trying {i+1} time:")
            session.cookies.clear()
            time.sleep(2**(i+1))
            headers['Referer'] = random.choice(referer)
            headers['User-Agent'] = ua.random
            response = session.get(url, headers=headers)
            if response.status_code == 200 or 'recaptcha' not in response.text:
                print('Successfully fetched the url.')
                soup = BeautifulSoup(response.text, 'lxml')
                break
            else:
                print('Still getting no valid response. Trying Again!')
                continue
        else:
            print('Max Retries tried. Check the HTML file.')
            with open('no_valid_response.html', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
    return soup


def get_links(soup):
    links = []
    a_tags = soup.find_all('a', class_='rPDeLR')
    for a_tag in a_tags:
        link = "https://www.flipkart.com" + a_tag['href']
        links.append(link)
    return links


def get_data(soup):
    width = None
    thickness = None
    height = None
    weight = None
    sales_package = None
    model_number = None
    model_name = None
    dial_shape = None
    strap_color = None
    touch_screen = None
    water_resistant = None
    sensor = None
    battery_type = None
    charge_time = None
    battery_life = None
    warranty = None
    warranty_service = None
    covered = None
    not_covered = None
    data = []
    try:
        title = soup.find('span', class_='VU-ZEz').text.strip()
    except AttributeError:
        title = ''

    try:
        current_price = soup.find('div', class_='Nx9bqj CxhGGd').text.strip()
    except AttributeError:
        try:
            current_price = soup.find('div', class_='Nx9bqj CxhGGd yKS4la').text.strip()
        except AttributeError:
            current_price = ''

    try:
        ratings_and_reviews = soup.find('span', class_='Wphh3N').find('span').find_all('span')
        rating = ratings_and_reviews[0].text.strip()
        review = ratings_and_reviews[2].text.strip()
    except AttributeError:
        rating = ''
        review = ''

    try:
        specifications = soup.find_all('div', class_='GNDEQ-')
        for specification in specifications:
            text = specification.find('div', class_='_4BJ2V+').text.strip()
            if text.lower() == 'dimensions':
                trs = specification.find('table').find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    try:
                        if tds[0].text.lower() == 'width':
                            width = tds[1].text.strip()
                    except AttributeError:
                        width = ''
                    try:
                        if tds[0].text.lower() == 'thickness':
                            thickness = tds[1].text.strip()
                    except AttributeError:
                        thickness = ''
                    try:
                        if tds[0].text.lower() == 'weight':
                            weight = tds[1].text.strip()
                    except AttributeError:
                        weight = ''
                    try:
                        if tds[0].text.lower() == 'height':
                            height = tds[1].text.strip()
                    except AttributeError:
                        height = ''
            if text.lower() == 'general':
                trs = specification.find('table').find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    try:
                        if tds[0].text.lower() == 'sales package':
                            sales_package = tds[1].text.strip()
                    except AttributeError:
                        sales_package = ''
                    try:
                        if tds[0].text.lower() == 'model number':
                            model_number = tds[1].text.strip()
                    except AttributeError:
                         model_number = ''
                    try:
                        if tds[0].text.lower() == 'model name':
                            model_name = tds[1].text.strip()
                    except AttributeError:
                        model_name = ''
                    try:
                        if tds[0].text.lower() == 'dial shape':
                            dial_shape = tds[1].text.strip()
                    except AttributeError:
                        dial_shape = ''
                    try:
                        if tds[0].text.lower() == 'strap color':
                            strap_color = tds[1].text.strip()
                    except AttributeError:
                        strap_color = ''
                    try:
                        if tds[0].text.lower() == 'touchscreen':
                            touch_screen = tds[1].text.strip()
                    except AttributeError:
                         touch_screen = ''
                    try:
                        if tds[0].text.lower() == 'water resistant':
                            water_resistant = tds[1].text.strip()
                    except AttributeError:
                        water_resistant = ''
            if text.lower() == 'product details':
                trs = specification.find('table').find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    try:
                        if tds[0].text.lower() == 'sensor':
                            sensor = tds[1].text.strip()
                    except AttributeError:
                        sensor = ''
                    try:
                        if tds[0].text.lower() == 'battery type':
                            battery_type = tds[1].text.strip()
                    except AttributeError:
                        battery_type = ''
                    try:
                        if tds[0].text.lower() == 'charge time':
                            charge_time = tds[1].text.strip()
                    except AttributeError:
                        charge_time = ''
                    try:
                        if tds[0].text.lower() == 'battery life':
                            battery_life = tds[1].text.strip()
                    except AttributeError:
                        battery_life = ''
            if text.lower() == 'warranty':
                trs = specification.find('table').find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    try:
                        if tds[0].text.lower() == 'warranty summary':
                            warranty = tds[1].text.strip()
                    except AttributeError:
                        warranty = ''
                    try:
                        if tds[0].text.lower() == 'warranty service type':
                            warranty_service = tds[1].text.strip()
                    except AttributeError:
                        warranty_service = ''
                    try:
                        if tds[0].text.lower() == 'covered in warranty':
                            covered = tds[1].text.strip()
                    except AttributeError:
                        covered = ''
                    try:
                        if tds[0].text.lower() == 'Not Covered in Warranty':
                            not_covered = tds[1].text.strip()
                    except AttributeError:
                        not_covered = ''
    except AttributeError:
        pass

    data.append({'Title': title,
                 'Price': current_price,
                 'Rating': rating,
                 'No. of Reviews': review,
                 'Width': width,
                 'Thickness': thickness,
                 'Weight': weight,
                 'Height': height,
                 'Sales Package': sales_package,
                 'model number': model_number,
                 'model name': model_name,
                 'Shape': dial_shape,
                 'Color': strap_color,
                 'Touchscreen?': touch_screen,
                 'Water resistant?': water_resistant,
                 'Sensor': sensor,
                 'Battery Type': battery_type,
                 'Charge Time': charge_time,
                 'Battery Life': battery_life,
                 'Warranty': warranty,
                 'Warranty Service Information': warranty_service,
                 'Covered in warranty': covered,
                 'Not covered in warranty': not_covered
                 })
    return data


def main():
    all_data = []
    links_queue = queue.Queue()
    base_url = 'https://www.flipkart.com/wearable-smart-devices/smart-watches/pr?sid=ajy%2Cbuh&marketplace=FLIPKART&page={}'

    def fetch_links(page_num):
        url = base_url.format(page_num)
        soup = get_soup_with_retry(url)
        links = get_links(soup=soup)
        print(f"Total Links found on page {page_num}: {len(links)}")
        for link in links:
            links_queue.put(link)

    def fetch_data():
        while not links_queue.empty():
            link = links_queue.get()
            start_time = time.time()
            soup = get_soup_with_retry(link)
            if soup:
                data = get_data(soup=soup)
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
            elapsed = time.time() - start_time
            print(f"Processed link in {elapsed:.2f} seconds: {link}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_links, range(1, 21))
        executor.map(lambda _: fetch_data(), range(30))# Adjust the range for speed.

    save_to_excel(all_data)
    save_to_json(all_data)
    save_to_csv(all_data)
    save_to_sqlite(all_data)


def save_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel('Flipkart_Smartwatches.xlsx', index=False)


def save_to_json(data):
    with open('Flipkart_Smartwatches.json', 'w') as f:
        json.dump(data, f, indent=4)


def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('Flipkart_Smartwatches.csv', index=False)


def save_to_sqlite(data):
    df = pd.DataFrame(data)
    conn = sqlite3.connect('Flipkart_Smartwatches.db')
    df.to_sql('smartwatches', conn, if_exists='replace', index=False)
    conn.close()


def info():
    print('This scraper is built by github.com/Abdullah-Shaheer')
    print("Scrapes watches information from flipkart")
    print('[+] Bulk Data')
    print('[+] Multi-threaded Code')
    print('[+] Fast Output')
    print('Going to start scraping in 5 seconds.')
    time.sleep(5)


if __name__ == '__main__':
    info()
    main()
