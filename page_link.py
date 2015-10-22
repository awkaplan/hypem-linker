#!/usb/bin/env python
import json
import argparse

from BeautifulSoup import BeautifulSoup
import requests

parser = argparse.ArgumentParser(description="Hypem song post URL.")
parser.add_argument('url', metavar='url', type=str)
args = parser.parse_args()

headers = {"Cookie": "AUTH=03%3Asomething%3Asomething%3Asomething%3ACA-US"}

bs = BeautifulSoup(requests.get(args.url, headers=headers).text)

for i in bs.findAll("script", type="application/json", id="displayList-data"):
    js = json.loads(i.next)
    trackurl = "http://hypem.com/serve/source/%s/%s" % (js['page_arg'], js['tracks'][0]['key'])
    print requests.get(trackurl, headers=headers).json()['url']
