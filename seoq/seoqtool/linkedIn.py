CONSUMER_KEY = '77sszs96fhv0c3'     # This is api_key
CONSUMER_SECRET = 'DwrBh7xffb5DaQmc'   # This is secret_key

RETURN_URL = 'https://www.seoq.com/'

from linkedin import linkedin

authentication = linkedin.LinkedInAuthentication(CONSUMER_KEY, CONSUMER_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print authentication.authorization_url
application = linkedin.LinkedInApplication(authentication)