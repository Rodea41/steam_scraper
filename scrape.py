
import requests
import lxml.html

html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)