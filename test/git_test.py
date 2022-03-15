import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from scrappers.git import GitScrapper


class TestGitScrapper(unittest.TestCase):
    # equivalent html like on github for repositories and language statistics
    html_for_repos = '<div class="f4 text-normal"><a class="v-align-middle"  href="/nginx/nginx">nginx</a></div>'
    html_for_languages = """
                            <a class="d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3">' \
                                <span>C</span>
                                <span>96.8%</span>
                            </a>
                            <a class="d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3">' \
                                <span>Vim Script</span>
                                <span>2.5%</span>
                            </a>
                         """

    def test_fetch_html(self):
        # allow real call to the github
        git_scrapper = GitScrapper()
        html_from_github = git_scrapper.fetch_html("nginx")
        soup = BeautifulSoup(html_from_github, features="html.parser")

        # fetch special meta tag from github
        meta_tag_with_site_name = soup.find("meta", {"property": "og:site_name", "content": "GitHub"})
        self.assertTrue(meta_tag_with_site_name)

    @patch('requests.get')
    def test_git_search(self, test_stubs):
        nginx_repository = {'url': 'https://github.com/nginx/nginx'}
        git_scrapper = GitScrapper()
        # mock request.get method return value
        test_stubs.return_value.text = self.html_for_repos

        repositories = git_scrapper.git_search("nginx")
        self.assertTrue(nginx_repository in repositories)

    @patch('requests.get')
    def test_get_extra_information(self, test_stubs):
        nginx_repository_with_extra_info = {'url': 'https://github.com/nginx/nginx',
                                            'extra': {'language_stats': {'C': '96.8%',
                                                                         'Vim Script': '2.5%'},
                                                      'owner': 'nginx'}}

        git_scrapper = GitScrapper()
        # mock request.get method return value
        test_stubs.return_value.text = self.html_for_repos
        repositories = git_scrapper.git_search("nginx")

        # equivalent html like on github for language statistics

        # mock request.get method return value
        test_stubs.return_value.text = self.html_for_languages

        extras = git_scrapper.get_extra_information(repositories)
        self.assertTrue(nginx_repository_with_extra_info in extras)

    @patch('requests.get')
    def test_git_search_with_html_parser(self, test_stubs):
        nginx_repository = {'url': 'https://github.com/nginx/nginx'}
        git_scrapper = GitScrapper()

        # mock request.get method return value
        test_stubs.return_value.text = self.html_for_repos

        repositories = git_scrapper.git_search_with_html_parser("nginx")
        self.assertTrue(nginx_repository in repositories)


if __name__ == "__main__":
    unittest.main()
