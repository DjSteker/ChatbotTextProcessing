# Christopher Reeves Web Scraping Tutorial
# simple web spider that returns array of urls.
# http://youtube.com/creeveshft
# http://christopherreevesofficial.com
# http://twitter.com/cjreeves2011

import urllib
import urlparse
import mechanize
import json
from bs4 import BeautifulSoup
from google import search


# formats the query for duckduckgo api usage
def getGudURL(query, API=1):
    if API:
        return "http://api.duckduckgo.com/?q=" + \
            query.replace(" ", "%20").replace("+", "%2B") + "&format=json"


# duckduckgo api - returns descriptions as seen in search engine and the
# url
def api_search(term):

    result = list()

    url = getGudURL(term)

    jtext = urllib.urlopen(url)
    return jtext

    resp = json.load(jtext)

    for related_topic in resp['RelatedTopics']:
        if 'Text' in related_topic.keys():
            text = related_topic['Text']
            if term.lower() in text.lower() and term.lower() != text.lower():
                data = dict()
                data['description'] = text
                data['source'] = url
                result.append(data)

    return result


# perform a google search for the term returning maxseeds URL results
def url_seeds(term, maxseeds):
    search_results = search(term, stop=maxseeds)
    seeds = list()
    for res in search_results:
        seeds.append(res)
        if len(seeds) >= maxseeds:
            break
    return seeds


# searches the document found at given url for
# <div>s or <p>s containig the given term
# returns list(entry) where entry is a dictionary with "source" (URL) and
# "description" keys
def get_relevant_html(url, term):
    bad_html = urllib.urlopen(url)
    soup = BeautifulSoup(bad_html, "html.parser")
    paragraphs = soup.findAll('p') + soup.findAll('div')
    result = list()
    for p in paragraphs:
        text = p.getText()
        entries = text.split("\n")
        for text in entries:
            if term.lower() in text.lower() and term.lower() != text.lower():
                data = dict()
                data['description'] = text
                data['source'] = url
                if data not in result:
                    result.append(data)
    return result


# main crawler body where <term> is the lookup word/phrase, <maxseeds> is the
# maximum numbers of google search results (urls) to crawl and
# <maxsuburls> is the maximum number of pages within the scope of the
# given url
def creep_and_crawl(term, maxseeds=3, maxsuburls=3):

    result = list(api_search(term))

    url_startpoints = url_seeds(term, maxseeds)
    # print url_startpoints
    # lines = open("seeds.txt", "r").readlines()
    # url_startpoints = [l[:-1] for l in lines]

    br = mechanize.Browser()

    for url in url_startpoints:
        urls = [url]
        visited = [url]

        while len(urls) > 0:
            try:
                br.open(urls[0])
                urls.pop(0)
                for link in br.links():
                    newurl = urlparse.urljoin(link.base_url, link.url)
                    # print newurl
                    if newurl not in visited \
                            and url in newurl \
                            and len(visited) < maxsuburls:
                        visited.append(newurl)
                        urls.append(newurl)
                        # print newurl
                    if (len(visited) > maxsuburls):
                        break
            except:
                # print "error"
                try:
                    urls.pop(0)
                except:
                    pass

        for rel_url in visited:
            # print rel_url
            try:
                for r in get_relevant_html(rel_url, term):
                    # print r
                    if r not in result:
                        # print type(result), type(r)
                        result.append(r)
            except:
                # print "malformed url"
                pass
    return result


# <term> is the lookup word/phrase,
# <maxseeds> is the maximum numbers of google search results (urls) to crawl
# <maxsuburls> is the maximum number of pages within the scope of the given url
# filters the results for possible invalid data
def term_lookup(term, maxseeds=3, maxsuburls=3):
    cr = creep_and_crawl(term, maxseeds, maxsuburls)
    result = list()
    for r in cr:
        try:
            # print "descriptioin:" + r["description"], "\nsource:" +
            # r["source"]
            data = dict()
            data["description"] = r["description"]
            data["source"] = r["source"]
            result.append(data)
        except:
            pass
    return result


tl = term_lookup("vasile")
for r in tl:
    print "descriptioin:" + r["description"], "\nsource:" + r["source"]
