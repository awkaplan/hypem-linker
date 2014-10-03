#!/usb/bin/env python
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import gzip
import json
import urllib2
import argparse

parser = argparse.ArgumentParser(description="Hypem song post URL.")
parser.add_argument('url', metavar='url', type=str)
args = parser.parse_args()

url = args.url

headers = {
    "Host" : "hypem.com",
    "Cookie" : "AUTH=03%3Asomething%3Asomething%3Asomething%3ACA-US",
    "Accept-Encoding" : "gzip,deflate,sdch",
    "Accept-Language" : "en-US,en;q=0.8",
    "User-Agent" : "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referrer" : "http://hypem.com",
    "X-Requested-With" : "XMLHttpRequest",
    "Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
}


init_req = urllib2.Request(url, None, headers=headers)
init_response = urllib2.urlopen(init_req)

init_buf = StringIO(init_response.read())
init_gz = gzip.GzipFile(fileobj=init_buf)

soup = BeautifulSoup(init_gz.read())

for i in soup.findAll("script",  type="application/json", id="displayList-data"):
    key_json = json.loads(i.getText())
    page_arg = key_json.get('page_arg')
    for j in key_json.get('tracks'):
        key = j.get('key')
        trackurl = "http://hypem.com/serve/source/%s/%s" % (page_arg,key)
        req = urllib2.Request(trackurl, None, headers=headers)
        resp = urllib2.urlopen(req)
        buf = StringIO(resp.read())
        f = gzip.GzipFile(fileobj=buf)
        mp3_json = json.loads(f.read())
        print mp3_json.get('url')
            
