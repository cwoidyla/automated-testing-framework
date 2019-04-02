'''
  Sample code for using requests to scrape web form data
  and Beautiful Soup to parse it.
'''

import requests
from bs4 import BeautifulSoup as soup

def main():
    my_url = "https://mysite-qual.com"
    un = ""
    pw = ""
    auth=(un,pw)
    r = requests.get(my_url, auth=auth)
    page_html = r.text
    page_soup = soup(page_html, "html.parser")
    print([tag.name for tag in page_soup.find_all()])
    print(page_soup.find('input', {'name': 'btCreate'}).get('value'))

def phs_site_auth(top_level_url):
    # create a password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    password_mgr.add_password(None, top_level_url, un, pw)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    # create "opener" (OpenerDirector instance)
    opener = urllib.request.build_opener(handler)
    # Install the opener.
    # Now all calls to urllib.request.urlopen use our opener.
    urllib.request.install_opener(opener)
    # use the opener to fetch a URL
    uClient = opener.open(top_level_url)
    page_html = uClinet.read()
    uClient.close()
    return page_html

    # auth.add_password(None, my_url, un, pw)
    # handler = urllib2.HTTPBasicAuthHandler(auth)
    # opener = urllib2.build_opener(handler)
    # urllib2.install_opener(opener)
    # uClient = urllib2.urlopen(url)
    # page_html = uClinet.read()
    # uClient.close()
    # return page_html


if __name__ == "__main__":
    main()
