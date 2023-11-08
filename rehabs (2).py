import re
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag
from requests import TooManyRedirects


def get_soup(_session: requests.Session, _url: str) -> BeautifulSoup:
    try:
        request_data = _session.get(_url, headers={"User-Agent": "Mozilla/5.0"})
    except TooManyRedirects:
        print(f"Too many redirects for {_url}")
        return BeautifulSoup()
    return BeautifulSoup(request_data.content, features="html.parser")


def get_href(tag: Tag, _url: str) -> Optional[str]:
    href = tag.get("href")
    if href is None:
        return None
    if href.startswith("http"):
        return href
    if not (_url.endswith("/") or href.startswith("/")):
        _url += "/"
    return f"{_url}{href}"


session = requests.Session()
url = input("What is the URL?")
item_link_container = input("What is the container type for item link?")
item_link_container_class = input("What is the item link container class?"
                                  "Leave blank to omit the class attribute")
name_container = input("What is the container type for name?")
name_container_class = input("What is the name container class? "
                             "Leave blank to omit the class attribute.")
website_container = input("What is the container type for website?")
website_container_class = input("What is the website container class?"
                                "Leave blank to omit the class attribute.")

# Example inputs
# url = "https://sobernation.com/rehab/new-hampshire/"
# item_link_container = "a"
# item_link_container_class = "uk-button sn-button button-1"
# name_container = "h1"
# name_container_class = "uk-margin-remove-top uk-text-capitalize uk-h1 uk-text-600 color-white"
# website_container = "a"
# website_container_class = "color-g"

# Example inputs
# url = "https://rehabs.com/local/california/"
# item_link_container = "a"
# item_link_container_class = "listing-details__name"
# name_container = "h1"
# name_container_class = ""
# website_container = "a"
# website_container_class = "jsx-c6827d4ce8453dc4"


base_url = re.match(r"^.+?[^\/:](?=[?\/]|$)", url).group()
item_link_kwargs = {}
name_kwargs = {}
website_kwargs = {"href": re.compile(f"(?=^(http))(?!^({base_url})).+")}
if item_link_container_class:
    item_link_kwargs["class"] = item_link_container_class
if name_container_class:
    name_kwargs["class"] = name_container_class
if website_container_class:
    website_kwargs["class"] = website_container_class

soup = get_soup(session, url)

item_links = soup.find_all(item_link_container, item_link_kwargs)

for item in item_links:
    soup = get_soup(session, get_href(item, base_url))
    if soup.find(name_container, name_kwargs):
        name = soup.find(name_container, name_kwargs).get_text()
    else:
        name = None
    if soup.find(website_container, website_kwargs):
        website = soup.find(website_container, website_kwargs).get("href")
    else:
        website = None
    print(f"Name: {name}")
    print(f"Website: {website}")
