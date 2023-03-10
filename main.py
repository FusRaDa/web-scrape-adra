import time
import json

from bs4 import BeautifulSoup
import requests
import configparser

parser = configparser.ConfigParser()
parser.read('config.txt')
class_category = parser.get('config', 'organization_type')
is_active = parser.get('config', 'is_active')
name = parser.get('config', 'search_term')

file_name = 'eAdventists_' + class_category + '.json'

with open(file_name, 'w') as empty_json:
    json.dump([], empty_json, indent=4)
    empty_json.close()


def get_class_from_category(string):
    if string == 'Conf/Union/Div':
        return 1
    elif string == 'Congregation':
        return 2
    elif string == 'School':
        return 3
    elif string == 'Conf/Union/Div Sub-Orgs':
        return 4
    elif string == 'Medical':
        return 5
    elif string == 'Media':
        return 6
    elif string == 'Publishing':
        return 7
    elif string == 'Foreign':
        return 8
    elif string == 'Unknown':
        return 9
    elif string == 'Congregation Sub-Orgs':
        return 10
    else:
        return 0


form_data = {
    'name': name,
    'class': get_class_from_category(class_category),
    'authenticity_token': 'DAXOl8nWaQv5NLV+OFRWVreESfiM4bbQm3B8rSMwaAc=',
    'is_active': is_active,
    'commit': 'Search',
}


def get_urls_list(html):
    links = []
    soup = BeautifulSoup(html, 'lxml')
    url_list = soup.find_all('tr', class_='results-line-1')
    for url in url_list:
        links.append(url.a['href'])
    return links


def write_json_data(data_dict):

    # read file
    with open(file_name, "r") as read:
        data = json.load(read)

    # update json object
    data.append(data_dict)
    print(data)

    # write json file
    with open(file_name, 'w') as write:
        json.dump(data, write, indent=4)


def scrape_data_from_url_page(url):
    time.sleep(4)

    full_url = 'https://eadventist.net' + url
    server = requests.post(full_url)
    status_code = server.status_code

    if status_code == 429:
        time.sleep(30)
        server = requests.post(full_url)

    html = server.text
    soup = BeautifulSoup(html, 'lxml')

    # Get Data and Transfer to Txt File
    title = soup.find('span', id='title')
    fields = soup.find_all('td', class_='field')
    labels = soup.find_all('label')

    field_array = []

    for field in fields:
        if field.a is not None:
            field_array.append(field.a['href'] + " " + field.text)
        else:
            field_array.append(field.text.replace('\xa0', ''))

    label_array = []

    for label in labels:
        label_array.append(label.text)

    data_dict = {'title': title.text}

    for i in range(len(label_array)):
        data_dict[label_array[i]] = field_array[i]

    write_json_data(data_dict)


def get_results_page(page):
    string_number = page.__str__()
    url = 'https://eadventist.net/en/search?page=' + string_number + '&type=a'

    time.sleep(4)  # avoid 429 too many requests - 4s seems to be the most optimal
    server = requests.post(url, data=form_data)
    status_code = server.status_code

    # handle 429 code
    if status_code == 429:
        time.sleep(30)
        server = requests.post(url, data=form_data)

    search_results_html = server.text

    url_list = get_urls_list(search_results_html)

    for url in url_list:
        scrape_data_from_url_page(url)

    return len(url_list)


def go_to_next_page():
    page = 1

    while get_results_page(page) > 0:
        print('yay')
        page += 1


go_to_next_page()
