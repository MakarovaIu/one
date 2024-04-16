import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_links(url):
    """ Gets a link to a website and collects all links from it to links list. """
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text, features="html.parser")
    links = []
    for link in soup.find_all("a"):
        links.append(link.get("href"))
    return links


def get_hosts(links):
    """ Gets all host names from a list of links and returns it sorted without duplicates. """
    host_set = set()
    for link in links:
        parsed_link = urlparse(link)
        hostname = parsed_link.hostname
        if hostname:
            host_set.add(hostname)
    hosts = list(host_set)
    return sorted(hosts)


def check_route(url1, url2):
    """ Gets all links from url1 then checks if any of these links leads to url2.
     Prints 'Yes' if so and 'No' otherwise. """
    links1 = get_links(url1)
    links = []
    for link in links1:
        links += get_links(link)
    print("Yes" if url2 in links else "No")


def get_two_links_from_user_input() -> list:
    urls = []
    for _ in range(2):
        url = input()
        urls.append(url.strip())
    return urls


def get_file_link() -> str:
    return input().strip()


def find_if_route_exists():
    url1, url2 = get_two_links_from_user_input()
    check_route(url1, url2)


def find_all_hosts():
    url = get_file_link()
    links = get_links(url)
    for host in get_hosts(links):
        yield host


if __name__ == '__main__':
    # find_if_route_exists()

    for i in find_all_hosts():
        print(i)




