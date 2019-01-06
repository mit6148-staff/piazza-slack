from piazza_api import Piazza
import json
import requests
import time

CLASS_ID = "jpwuh5je670578"

p = Piazza()
p.user_login(email="piazza-bot@mit.edu", password="piazza-bot")

user_profile = p.get_user_profile()
weblab = p.network(CLASS_ID)

last_post = 0 # most recent post sent to slack

def get_url(post):
    return "https://piazza.com/class/{}?cid={}".format(CLASS_ID, post['nr'])

def iter_posts():
	for post in weblab.get_feed(limit=999999, offset=0)['feed']:
		yield post

while True:
	print("polling piazza")
	posts_sent = []
	for post in iter_posts():
		if post['nr'] <= last_post:
			continue

		posts_sent.append(post['nr'])	
		data = {
			"username": "Piazza Bot",
			"icon_url": "https://pbs.twimg.com/profile_images/1419243630/twitter_pic_400x400.png",
			"attachments": [
				{
					"fallback": get_url(post),
					"color": "#36a64f",
					"title": post['subject'],
					"title_link": get_url(post),
					"text": post['content_snipet']
				}
			],
		}
		
		r = requests.post("https://hooks.slack.com/services/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", data=json.dumps(data))
		print(r)

	last_post = max(posts_sent + [last_post])
	time.sleep(5)
