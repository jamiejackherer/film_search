#!/usr/bin/env python3

import re, os, time, requests, threading, binascii
import jsbeautifier
from bs4 import BeautifulSoup as bs

url = "http://vidzi.tv/15vzx7hzbu76.html"
# url = "http://vidto.me/jd45t9kk820k.html"
# url = input("[+] Please enter the url to extract the video from: ")
print("[+] Using url\n", url)
print("[+] Fetching webpage")

headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}
r = requests.get(url, headers=headers)

s = bs(r.text, "lxml")

print("[+] Finding javascript in page")
find_js = s.find("script", attrs={"type": "text/javascript", "src": "http://static.vidzi.tv/nplayer/jwplayer.js"})

print("[+] Finding next sibling in page")
ob_js = find_js.find_next_sibling()

print("[+] Deobfuscating javascript")
js = jsbeautifier.beautify(str(ob_js.text))
print(js)
print("[+] Regexing a link")

pattern = re.compile("(http.*(?:\.mp4))")
link_re = pattern.findall(js)
for x in link_re:
    link = x
    print("[+] We found a link;\n\t{0}".format(link))

# TODO get a title for the video
download_dict = [{"link_name": "get_title.mp4", 
                  "link_address": link},]


# Downloader class - reads queue and downloads each file in succession
class Downloader(threading.Thread):
    """Threaded File Downloader"""

    def __init__(self, queue, output_directory):
            threading.Thread.__init__(self, name=binascii.hexlify(os.urandom(16))) 
            # might need to append .decode() for str obj not bytes obj
            self.queue = queue
            self.output_directory = output_directory

    def run(self):
        while True:
            # gets the url from the queue
            url = self.queue.get()

            # download the file
            print("* Thread {0} - processing URL".format(self.name))
            self.download_file(url)

            # send a signal to the queue that the job is done
            self.queue.task_done()

    def download_file(self, url):
        t_start = time.clock()

        r = requests.get(url)
        if (r.status_code == requests.codes.ok):
            t_elapsed = time.clock() - t_start
            print("* Thread: {0} Downloaded {1} in {2} seconds".format(self.name, url, str(t_elapsed)))
            fname = self.output_directory + "/" + os.path.basename(url)

            with open(fname, "wb") as f:
                f.write(r.content)
        else:
            print("* Thread: {0} Bad URL: {1}".format(self.name, url))

# Spawns dowloader threads and manages URL downloads queue
class DownloadManager():

    def __init__(self, download_dict, output_directory, thread_count=5):
        self.thread_count = thread_count
        self.download_dict = download_dict
        self.output_directory = output_directory

    # Start the downloader threads, fill the queue with the URLs and
    # then feed the threads URLs via the queue
    def begin_downloads(self):
        import queue
        queue = queue.Queue()

        # Create a thread pool and give them a queue
        for i in range(self.thread_count):
            t = Downloader(queue, self.output_directory)
            t.setDaemon(True)
            t.start()

        # Load the queue from the download dict
        for linkname in self.download_dict:
            # print(uri)
            queue.put(self.download_dict[linkname])

        # Wait for the queue to finish
        queue.join()

        return


download_manager = DownloadManager(link, "/mp4_dls", 5)
download_manager.begin_downloads()
