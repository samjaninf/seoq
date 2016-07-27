import whois
import requests
from urlparse import urlparse
from builtwith import builtwith
# http://stackoverflow.com/questions/9626535/get-domain-name-from-url


def get_expiration_and_creation_date(url):
    if 'https' in url or 'http' in url:
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        domain = domain.replace(
            'https://', '').replace('http://', '').replace('/', '')
    else:
        domain = str(url)
    try:
        url_information = whois.query(domain)
    except Exception:
        return None, None
    if url_information is None:
        return None, None
    return url_information.creation_date, url_information.expiration_date


def get_built_with_information(url):
    if 'http://' not in url and 'https://' not in url:
        url = 'http://' + url
    try:
        return builtwith(url)
    except Exception:
        try:
            url = url.replace('http://', 'https://')
            return builtwith(url)
        except Exception as e:
            return {'error': e}


def get_total_time_and_ssl_certification(url):
    url = url.replace(
        'www.', '').replace(
        'http://', 'https://').replace('https://', 'https://www.')
    if 'https://www.' in url:
        ssl_certificate = True
    else:
        ssl_certificate = False
    if 'http://www.' not in url and 'https://www.' not in url:
        url = 'https://www.' + url
    try:
        response = requests.get(url)
        ssl_certificate = True
    except (requests.exceptions.SSLError,
            requests.exceptions.ConnectionError):
        ssl_certificate = False
        try:
            url = url.replace('https://', 'http://')
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return {'connection_error': 'connection_error'}
    return {'ssl_certificate': ssl_certificate,
            'speed_info': {
                'time_in_seconds': response.elapsed.total_seconds(),
                'history': response.history
            }
            }
