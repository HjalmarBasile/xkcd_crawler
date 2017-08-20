#!/usr/bin/env python3

import os
import os.path

import requests # http requests
from bs4 import BeautifulSoup # html parser

# Utility to print to stdout and write to file the same string
def print_log(s):
    print(s)
    logf.write(s + '\n')


# The pics will be stored in memory in the following folder
xkcd_fold = os.path.expanduser('~') + '/xkcd_pics/'
if not os.path.exists(xkcd_fold):
    os.mkdir(xkcd_fold)

# Log file to keep track of strips different from usual
logf = open(xkcd_fold + 'readme.log', 'w')

i = 0
while True:
    i += 1

    # Meta strip
    if i == 404:
        print_log("404 Not Found")
        continue

    # Request the web page and prepare it for parsing
    url = 'https://xkcd.com/' + str(i) + '/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    strip_title = soup.title.string[6:]

    # The pic infos can be found in the "comic" div
    comic_div = soup.find(id="comic")
    pic = comic_div.img

    # Skip some edge cases: not all xkcd strips are simple pics
    if comic_div.script:
        print_log("Strip " + str(i) + " contains scripts: skipping")
        continue
    if not pic:
        print_log("Could not find pic for strip " + str(i) + ": skipping")
        continue

    pic_url = "https:" + pic.get('src')
    pic_ext = '.' + pic_url.split('.')[-1]

    if comic_div.a:
        print_log("Check the web page of strip " + str(i) + " for more details about it (open pic link)")

    # The pic will be stored in memory with the following name
    pic_name = '{:04d}'.format(i) + ' - ' + strip_title + pic_ext
    pic_name = pic_name.replace('/','_')

    with open(xkcd_fold + pic_name, 'wb') as picf:
        picf.write(requests.get(pic_url).content)

    print("pic " + '{:04d}'.format(i) + " done")

    # Check if continue
    nexti = soup.find(class_="comicNav").find(rel="next").get('href')
    if nexti == '#':
        break

logf.close()
print ("Congratulations, now the entire (or almost) xkcd collection is stored in your pc!")
