# hardcoded version of github repository scraper
# can have advantages over third party libraries by stopping
# parsing process when expected data is found

from parsers.html_parser import ParsePages


class ParseRepositories(ParsePages):

    def __init__(self, tag_name, class_name, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.tag_name = tag_name
        self.class_name = class_name
        self.flag = False
        self.list = []

    def handle_starttag(self, tag, attrs):
        if self.flag:
            self.list.append(
                {"url": f"https://github.com{attrs[-1][1]}"})  # or py parsing out from data-hydro-click attr
            self.flag = False
        elif tag == self.tag_name and ("class", self.class_name) in attrs:
            self.flag = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def feed(self, data):
        ParsePages.feed(self, data)
        return self.list
