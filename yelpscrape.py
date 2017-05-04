from bs4 import BeautifulSoup
import requests
import sys
import csv
import re
from time import time
from datetime import datetime

print ('*'*30)

url = input("Enter the name of the file to be scraped:")
with open(url, encoding="utf-8") as infile:
	soup = BeautifulSoup(infile, "html.parser")

print ('*'*30)

tzvar = int(input("\n\nTimestamps in Twitter are determined by the user's location.\n\nIf you are searching for tweets connected to an event in a specific location, you can edit the timestamp here in order to match tweet times to the local time of an event. Use a negative number, with a - symbol, when subtracting hours.\n\nEnter the number of hours you'd like to add to or subtract from the timestamp:"))
tzvarsecs = (tzvar*3600)
#print (tzvarsecs)

def timestamp_to_str(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %m/%d/%Y')

#url = 'https://twitter.com/search?q=%23bangkokbombing%20since%3A2015-08-10%20until%3A2015-09-30&src=typd&lang=en'
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
#r = requests.get(url, headers=headers)
#data = r.text.encode('utf-8')
#soup = BeautifulSoup(data, "html.parser")

names = soup('strong', {'class': 'fullname js-action-profile-name show-popup-with-id'})
usernames = [name.contents[0] for name in names]

handles = soup('span', {'class': 'username js-action-profile-name'})
userhandles = [handle.contents[1].contents[0] for handle in handles]  
athandles = [('@')+abhandle for abhandle in userhandles]

links = soup('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})
urls = [link["href"] for link in links]
fullurls = [permalink for permalink in urls]

timestamps = soup('span', {'class': '_timestamp js-short-timestamp '})
dtinfo = [timestamp["data-time"] for timestamp in timestamps]
times = map(int, dtinfo)
adjtimes = [x+tzvarsecs for x in times]
adjtimesfloat = [float(i) for i in adjtimes]
dtinfofloat = [float(i) for i in dtinfo]
finishedtimes = [x for x in map(timestamp_to_str, adjtimesfloat)]
originaltimes = [x for x in map(timestamp_to_str, dtinfofloat)]

messagetexts = soup('p', {'class': 'TweetTextSize  js-tweet-text tweet-text'}) 
messages = [messagetext for messagetext in messagetexts]  

retweets = soup('button', {'class': 'ProfileTweet-actionButtonUndo js-actionButton js-actionRetweet'})
retweetcounts = [retweet.contents[3].contents[1].contents[1].string for retweet in retweets]

favorites = soup('button', {'class': 'ProfileTweet-actionButtonUndo u-linkClean js-actionButton js-actionFavorite'})
favcounts = [favorite.contents[3].contents[1].contents[1].string for favorite in favorites]

images = soup('div', {'class': 'content'})
imagelinks = [src.contents[5].img if len(src.contents) > 5 else "No image" for src in images]

#print (usernames, "\n", "\n", athandles, "\n", "\n", fullurls, "\n", "\n", datetime, "\n", "\n",retweetcounts, "\n", "\n", favcounts, "\n", "\n", messages, "\n", "\n", imagelinks)

rows = zip(usernames,athandles,fullurls,originaltimes,finishedtimes,retweetcounts,favcounts,messages,imagelinks)

rownew = list(rows)

#print (rownew)
print ('*'*30)
newfile = input("\n\nEnter a filename for the csv file.\n\nPlease do not include the file extension, it will be appended automatically.\n\nAdditionally, this script will automatically overwrite any files that currently exist in the working directory,\nso please be careful when selecting filenames.\n\nEnter filename:") + ".csv"

with open(newfile, 'w', encoding='utf-8') as f:
	writer = csv.writer(f, delimiter=",")
	writer.writerow(['Usernames', 'Handles', 'Urls', 'User Timestamp', 'Adjusted Event Timestamp', 'Retweets', 'Favorites', 'Message', 'Image Link'])
	for row in rownew:
		writer.writerow(row)

