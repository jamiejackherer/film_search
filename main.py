#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup as bs

pre_url = str("https://primewire.unblocked.onl")

ask_for_keywords = input("[+] What do you want to search for?: ")
keywords_strip = ask_for_keywords.strip()
keywords = keywords_strip.replace(" ", "+")

# Ask which section you wanna use - section 1 is films - section 2 is tv
section = input("[+] Are you searching for Films or TV Shows?: ")
films_re = re.match("(([f|F])|([i|I])|([l|L])|([m|M])([s|S]).?)", section)
tv_re = re.match("(t|T)|(v|V)|[ ]|(s|S)|(h|H)|(o|O)|(w|W)|(s|S)?", section)
if films_re:
    print("[+] Searching Films... Please wait...")
    section = "1"
if tv_re:
    print("[+] Searching TV Shows... Please wait...")
    section = "2"


url = pre_url + str("/index.php?search_keywords=") + keywords + str("&search_section=") + section




# video link regex - (^http(s?):\/\/[0-9a-z\.]+\/([a-zA-Z0-9]+)\/).*(?:mp4$)
