import requests
import random
import re
from bs4 import BeautifulSoup
from typing import Sequence
from parsers.repository_parser import ParseRepositories


class GitScrapper:
    def __init__(self, search_type: str = "repositories", proxies: Sequence[dict] = None, tag_name: str = "div",
                 class_name: str = "f4 text-normal"):
        self.search_type = search_type
        self.proxies = proxies
        self.tag_name = tag_name
        self.class_name = class_name
        self.url = 'https://github.com/search'

    def fetch_html(self, keyword):
        # get raw html from github search page
        params = {"q": keyword, "type": self.search_type}
        if self.proxies:
            response = requests.get(self.url, params=params, proxies=random.choice(self.proxies))
        else:
            response = requests.get(self.url, params=params)

        return response.text

    # search git hub repositories by default
    def git_search(self, keyword: str) -> list:
        repositories = []
        html = self.fetch_html(keyword)

        # make parser
        soup = BeautifulSoup(html, features="html.parser")

        # find and loop repositories with special class
        for tag in soup.find_all(self.tag_name, {"class": self.class_name}):
            # or by parsing out from data-hydro-click attr
            link = tag.find("a")
            repositories.append({"url": f"https://github.com{link.get('href')}"})

        return repositories

    # set language statistics and owner from expected list of github urls
    def get_extra_information(self, sequence_of_urls: Sequence[dict]) -> Sequence[dict]:
        repositories_with_extra_data = sequence_of_urls[:]

        for url in repositories_with_extra_data:
            # set owner from url (Ex. nginx/nginx; owner is first "nginx" before /)
            owner = re.findall("github\.com\/([\w-]+)", url["url"])[0]
            url["extra"] = {"owner": owner, "language_stats": {}}

            if self.search_type == "repositories":
                response = requests.get(url["url"])
                soup = BeautifulSoup(response.text, features="html.parser")

                # find two span tags and fetch data
                for tag in soup.find_all("a", {
                    "class": "d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3"}):
                    spans = tag.find_all("span")
                    url["extra"]["language_stats"][spans[0].string] = spans[1].string

        return repositories_with_extra_data

    def git_search_with_html_parser(self, keyword: str) -> list:
        html = self.fetch_html(keyword)
        html_parser = ParseRepositories(self.tag_name, self.class_name, convert_charrefs=0)
        repositories = html_parser.feed(html)

        return repositories
