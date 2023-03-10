from bs4 import BeautifulSoup
import requests
import configparser

parser = configparser.ConfigParser()
parser.read('config.txt')
class_category = parser.get('config', 'organization_type')
is_active = parser.get('config', 'is_active')




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


def get_urls_list(html):
    soup = BeautifulSoup(html, 'lxml')
    url_list = soup.find_all('tr', class_='results-line-1')
    for url in url_list:
        link = url.a['href']
        print(link)


def gather_from_page():

    url = 'https://eadventist.net/en/search?page=1&type=a'

    form_data = {
        'class': get_class_from_category(class_category),
        'authenticity_token': 'DAXOl8nWaQv5NLV+OFRWVreESfiM4bbQm3B8rSMwaAc=',
        'is_active': is_active,
        'commit': 'Search',
    }

    server = requests.post(url, data=form_data)
    search_results_html = server.text

    get_urls_list(search_results_html)


gather_from_page()

