#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup as bs

pre_url = str("https://primewire.unblocked.onl")

ask_for_keywords = input("[+] What do you want to search for?: ")
keywords_strip = ask_for_keywords.strip()
keywords = keywords_strip.replace(" ", "+")

section = input("[+] Are you searching for Films or TV Shows?: ")



url = pre_url + str("/index.php?search_keywords=") + keywords + str("&search_section=") + section

