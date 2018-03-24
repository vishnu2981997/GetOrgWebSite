"""
GetOrgWebSite - Given the name of a company, fetches the website.
"""
import ssl
import urllib
import webbrowser
from bs4 import BeautifulSoup
import requests
import validators


def getorgi(name):
    """
    :param name: Takes company link as a string.
    :return: First possible link of the company when searched.
    """

    name = name.replace(" ", "+")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:

        requests.get("https://www.bing.com/search?q="+name, timeout=10)

    except requests.Timeout:

        print("timeout")
        exit()

    # Performing bing search on the given company name

    try:

        html = urllib.request.urlopen("https://www.bing.com/search?q="+name, context=ctx).read()
        soup = BeautifulSoup(html, "lxml")

    except ConnectionRefusedError:

        print("No results found")
        exit()

    # Fetching possible company links

    links = soup.find("ol").find_all("a", href=True)
    links = [i["href"] for i in links]

    return links[0]


def main():
    """
    :return: Null
    """
    company_name = input()
    url = getorgi(company_name)

    # Checking if url exists or not

    if validators.url(url):

        try:

            requests.get(url, timeout=10)
            webbrowser.open(url)

        except requests.Timeout:

            print("Timeout")
            exit()

    else:

        print("No page found")
        exit()


if __name__ == "__main__":
    main()
