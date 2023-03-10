import time

from bs4 import BeautifulSoup
import requests
import configparser

parser = configparser.ConfigParser()
parser.read('config.txt')
class_category = parser.get('config', 'organization_type')
is_active = parser.get('config', 'is_active')
name = parser.get('config', 'search_term')


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


def scrape_data_from_url_page(html):
    return "hi"


def get_results_page(page):
    string_number = page.__str__()
    url = 'https://eadventist.net/en/search?page=' + string_number + '&type=a'

    time.sleep(5)  # avoid 429 too many requests

    server = requests.post(url, data=form_data)
    search_results_html = server.text

    status_code = server
    print(status_code)

    url_list = get_urls_list(search_results_html)

    # for url in url_list:
    #     # add scrape data method here
    #     print(url)

    return len(url_list)


def go_to_next_page():
    page = 1

    while get_results_page(page) > 0:
        print('yay')
        page += 1

go_to_next_page()
