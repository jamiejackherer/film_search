#!/usr/bin/env python3

import re
import requests
import jsbeautifier
from bs4 import BeautifulSoup as bs

url = "http://vidzi.tv/15vzx7hzbu76.html"
#url = "http://vidto.me/jd45t9kk820k.html"
#url = input("[+] Please enter the url to extract the video from: ")
print("[+] Using url\n", url)
print("[+] Fetching webpage")

headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}
r = requests.get(url, headers=headers)

s = bs(r.text, "lxml")
#print(s)
print("[+] Finding javascript in page")
find_js = s.find("script", attrs={"type": "text/javascript", "src": "http://static.vidzi.tv/nplayer/jwplayer.js"})
#print(find_js.text)
print("[+] Finding next sibling in page")
ob_js = find_js.find_next_sibling()
#print(ob_js.text)
print("[+] Deobfuscating javascript")
js = jsbeautifier.beautify(str(ob_js.text))
print(js)
print("[+] Regexing a link")

pattern = re.compile(u"(http.*(?:\.mp4))")
link_re = pattern.findall(js)
for x in link_re:
    link = x
    print("[+] We found a link;\n\t{0}".format(link))
