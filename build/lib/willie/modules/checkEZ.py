# -*- coding: utf8 -*-
"""
checkEZ.py - Checks EZ for any new posts.
Copyright 2015, http://evilzone.org

Licensed under the Evilzone Forum License.
EZbot: https://evilzone.org
"""
#consider logining into forum

#import willie.web as web
from willie.module import interval, priority
import urllib2

#FIXME: Use bot.memory to cache last message.
lastMessage = 1
channels = ['#forum', '#testbot']

@interval(30)
@priority('high')
def checkEZ(bot):
	global lastMessage
	# threading.Timer(30.0, checkEZ).start()
	response = ""
	html = ""
	postlink = ""
	lastpost = ""
	newpage = ""
	title = ""
	try:
		response = urllib2.urlopen('https://evilzone.org/index.php')
	except Exception:
		return
	html = response.read()
	postlink = html.split("<dl id=\"ic_recentposts\" class=\"middletext\">\n\t\t\t\t\t<dt><strong><a href=\"")[1].split("/?topicseen;PHPSESSID")[0]
	lastpost = postlink.split("/msg")[-1]
	poster_name = html.split("ic_recentposts")[1].split("</a>")[1].split('>')[-1]
	if (lastMessage < lastpost):
		lastMessage = lastpost
		for channel in channels:
			if channel in bot.channels:
	        		bot.msg(channel, "New post by %s: %s/?topicseen#msg%s" %(poster_name, postlink, lastpost))
