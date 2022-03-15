# Crawler - Python GitHub Scrapper

Crawler has two scrapping implementations

1. It uses BeautifulSoup library to parse html
2. Custom class inheriting from build-in HTMLParser

# Advantages and Disadvantages
 ### BeautifulSoup
    with this library we can skip many parts of parsing the html 
    and writing search engines for that data, but it has to parse 
    all the html and then we can get all the information we need, 
    so it might take extra time to work with large htmle data
 ### Custom Parser
    by parsing the html using custom parsers, it takes more manual
    work, but instead we can control the whole parsing process and
    for example stop the parsing when we already have the information we want

# Run Scrapper
 more convenient way to run main.py is

    pipenv run python main.py

 Or you can run main.py after ```pipenv shell``` command.
 You can pass proxies to the GetScrapper constructor to make requests through them.
 Free list of proxies to work with at https://free-proxy-list.net/
    
    from pprint import pprint
    from scrappers.git import GitScrapper
    
    proxies = [
        {'http': 'http://213.226.11.149:41878', 'https': 'https://213.226.11.149:41878'},
        {'http': 'http://168.196.211.10:55443', 'https': 'https://168.196.211.10:55443'},
        {'http': 'http://46.0.203.186:8080', 'https': 'https://46.0.203.186:8080'},
    ]
    
    keyword = input("Search in github repositories: ")
    
    git = GitScrapper() # or GitScrapper(proxies=proxies)
    repositories = git.git_search(keyword)
    print("Get repositories with BeautifulSoup")
    pprint(repositories)
    print()
    
    print("Get extra information")
    pprint(git.get_extra_information(repositories))
    print()
    
    print("Get repositories with custom parser")
    pprint(git.git_search_with_html_parser(keyword))
    
 the output will be as follows
    
    Search in github repositories: nginx
    Get repositories with BeautifulSoup
    [{'url': 'https://github.com/nginx/nginx'},
     {'url': 'https://github.com/kubernetes/ingress-nginx'},
     {'url': 'https://github.com/sous-chefs/nginx'},
     {'url': 'https://github.com/nginx-proxy/nginx-proxy'},
     {'url': 'https://github.com/dockerfile/nginx'},
     {'url': 'https://github.com/arut/nginx-rtmp-module'},
     {'url': 'https://github.com/taobao/nginx-book'},
     {'url': 'https://github.com/nginxinc/kubernetes-ingress'},
     {'url': 'https://github.com/nginxinc/NGINX-Demos'},
     {'url': 'https://github.com/digitalocean/nginxconfig.io'}]
    
    Get extra information
    [{'C': '96.8%',
      'Vim Script': '2.5%',
      'extra': 'nginx',
      'url': 'https://github.com/nginx/nginx'},
       ....]
    
    Get repositories with custom parser
    [{'url': 'https://github.com/nginx/nginx'},
     {'url': 'https://github.com/kubernetes/ingress-nginx'},
     {'url': 'https://github.com/sous-chefs/nginx'},
     {'url': 'https://github.com/nginx-proxy/nginx-proxy'},
     {'url': 'https://github.com/dockerfile/nginx'},
     {'url': 'https://github.com/arut/nginx-rtmp-module'},
     {'url': 'https://github.com/taobao/nginx-book'},
     {'url': 'https://github.com/nginxinc/kubernetes-ingress'},
     {'url': 'https://github.com/nginxinc/NGINX-Demos'},
     {'url': 'https://github.com/digitalocean/nginxconfig.io'}]
 
# Install
 We use Docker to make installation easier
 
 ### Steps
  first create docker image(this command will automatically run tests too)

    docker build  -t crawler .
  
  after just run container with interactive mode
    
    docker container run -it crawler

  this command will run main.py, and you will see the output like this

    Search in github repositories: <keyword>
  
  and that's it :)

# Tests
 Tests are run with docker build command, however you can run tests directly, 
 but you have to take care of your configurations PYTHONPATH

# TODO
    1. we skip implementation for fetching extra information py using
       custom parsers and took advantage of BeautifulSoup.
       Depending on some use cases, we can add them too.
    2. use pytest for running tests and test coverage libs
    3. test for different types of requests(repositores, issues, wikis)
    4. reduce functions scope and make tham more smaller, flexible
