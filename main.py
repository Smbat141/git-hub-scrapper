from pprint import pprint
from scrappers.git import GitScrapper

proxies = [
    {'http': 'http://213.226.11.149:41878', 'https': 'https://213.226.11.149:41878'},
    {'http': 'http://168.196.211.10:55443', 'https': 'https://168.196.211.10:55443'},
    {'http': 'http://46.0.203.186:8080', 'https': 'https://46.0.203.186:8080'},
]

keyword = input("Search in github repositories: ")

# # search by wikis
# git = GitScrapper(search_type="wikis")  # or GitScrapper(proxies=proxies)

# # search by issues
# git = GitScrapper(search_type="issues", class_name="f4 text-normal markdown-title")  # or GitScrapper(proxies=proxies)

# search by repositories(by default)
git = GitScrapper()  # or GitScrapper(proxies=proxies)

repositories = git.git_search(keyword)
print("Get repositories with BeautifulSoup")
pprint(repositories)
print()

print("Get extra information")
pprint(git.get_extra_information(repositories))
print()

print("Get repositories with custom parser")
pprint(git.git_search_with_html_parser(keyword))






