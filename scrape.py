
from hashlib import new
from turtle import title
import requests
import lxml.html

html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)


"""Navigate to the New Releases tab"""
#Extract the div which contains the "popular new release" Tab
#Returns a lists of all the divs in the html page
#which have id of tab_newreleases_content.
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]


"""Extract the titles in New Releases tab"""
# '.' tells lxml that we are only interested in the tags which are children in the 'new_releases tag'
# [@class="tab_item_name"] filters through divs that contain class = tab_item_name
# /text() tells lxml that we only want the text contained within the tag we extracted
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
#print(titles)


"""Extract the price for each game"""
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')
#print(prices)

"""Extract the tags"""
#grab all the divs containing the tags for the games. Store them in tags_divs
tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = []

#loop through the list of extracted tags stored in tags_divs, 
#pull the text contained within the tags with text.content() method
#store the extracted text in the tags list with the .append() method
for div in tags_divs:
    tags.append(div.text_content())

"""Extract Tags using list comprehension""" 
#Use list comprehension or the method above
#tags = [tag.text_content() for tag in new_releases.xpath('.//div[@class="tab_item_top_tags"]')]

"""Seperating the tags in a list, so each tag is a seperate element"""
#List comprehension that tags each element in tags and seperates them with
#a comma and space 
tags = [tag.split(', ') for tag in tags]

"""Extracting the platforms"""
#First need to extract the divs with the tab_items_details class
#2nd extract the spans containing the platform_img class
#3rd extract the second class name from those spans
platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []

#Use [contains(@class, "platform_img")] instead of [@class ="platform_img"]
#because if the class contains multiple 'names' it won't be returned
#Using a list comprehension to reduce the code size
#.get() extracts the attribute of a tag, specifically the 'class' attr. if a 'span'
#.remove() removes the 'hmd.separator' text from platforms if it exists
for game in platforms_div:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd.separator' in platforms:
        platforms.remove('hmd_separator')
    total_platforms.append(platforms)



"""Putting everything together"""
#Using the zip() function to iterate over all of the lists in parrallel.
#Then we create a dictionary for each game and assign title, price, tags, platforms each as a separate key
#Last, append the dictionary to the 'output' list
output = [] 
for info in zip(titles,prices, tags, total_platforms):
    resp = {}                   #Initialize empty dict
    resp['title'] = info[0]     #First key in dict will be titles
    resp['price'] = info[1]     #second key will be price
    resp['tags'] = info[2]
    resp['platforms'] = info[3]
    output.append(resp)


print(output)


""""
-------------
TO DO LIST
-------------
1. Have output written to a text or csv file

"""