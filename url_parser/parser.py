from urlextract import URLExtract
import requests
import urllib
import warnings

class UrlParser:
    shorteners = ['bit.ly', 'cutt.ly', 'inf.im', 't1p.de', 'tinyurl.com', 'tiny.one', 'goo.gl']

    def __init__(self):
        self.extractor = URLExtract()
        self.session = requests.Session()

    def extract_urls(self, text: str, resolve_shortened: bool = False) -> list[str]:
        """Extract urls from text body, optionally resolve shortened urls
        :param text: text to extract urls from
        :param resolve_shortened: if True, resolves shortened urls
        :returns: a list of urls
        """
        urls = self.extractor.find_urls(text)
        processed_urls = []
        for url in urls:
            if 'http' not in url:
                url = 'https://' + url
            if resolve_shortened:
                for sh in self.shorteners:
                    if sh in url:
                        try:
                            resp = self.session.head(url, allow_redirects=True, verify=False)
                            url = resp.url
                        except:
                            warnings.warn(f'Could not resolve shortened URL {url}')
                        break
            processed_urls.append(url)
        return processed_urls


    def extract_sites(self, text):
        """
        Returns lists of sites (including TG/FB groups and channels)
        :param text: text to extract urls from
        :returns: a list of urls
        """
        sites = []
        full_urls = self.extract_urls(text, resolve_shortened=True)

        if len(full_urls) > 0:
            for url in full_urls:
                site = urllib.parse.urlparse(url).netloc
                if 'http' not in site:
                    site = 'https://' + site
                sites.append(site)
        return sites
