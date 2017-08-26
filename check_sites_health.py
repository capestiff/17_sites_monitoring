import requests
import whois
import datedelta
from pathlib import Path
from datetime import datetime


def load_urls4check(path_to_file):
    with open(path_to_file, 'r') as file:
        url_list = file.readlines()
    return [url_.strip('\n') for url_ in url_list]


def is_server_respond_with_200(url_):
    request = requests.get(url_)
    status_code = request.status_code

    if status_code == 200:
        return True
    else:
        return False


def get_domain_expiration_date(domain_url):
    domain = whois.whois(domain_url)
    return domain.expiration_date


def is_file(str_input):
    if Path(str_input).is_file():
        return True
    else:
        print('Please, verify the path and filename')
        return False


def check_urls_for_status_and_expdate(filepath_):
    link_list = load_urls4check(filepath_)

    for url in link_list:
        if is_server_respond_with_200(url):
            expiration_date = get_domain_expiration_date(url)
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            if (expiration_date - datedelta.MONTH) > datetime.now():
                print(url, 'HTTP 200 - OK, paid over a month - ', expiration_date)
            else:
                print(url, 'HTTP 200 - OK, paid under a month - ', expiration_date)
        else:
            print(url, 'ERROR')

if __name__ == '__main__':
    filepath = ''
    while not is_file(filepath):
        filepath = input('Enter the path to the file, containing URLs for checking: ')

    check_urls_for_status_and_expdate(filepath)
