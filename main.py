import sys
from urllib import urlencode
import requests
from urlparse import urlparse, parse_qs
import time

def checkCommentEligibility(contentData,pageAccessToken):
	commentUrl = 'https://graph.facebook.com/v2.1/%s/comments' % contentData['id']
	params = {'access_token': pageAccessToken}
	url = "%s?%s" % (commentUrl, urlencode(params))
	req = requests.get(url)
	if req.status_code == 200 :
		content = req.json()
		if not content['data']:
			return 1
		else:
			return 0
	else:
		print "\n\nUnable to connect. Check if session is still valid\n\n"

#Get Details of feed , page , comments or any other nodes of facebook
def getDetails(accessToken, url, parameter=None, value=None, ID=None):
	params = {'access_token': accessToken}
	getURL = '%s?%s' % (url, urlencode(params))
	req = requests.get(getURL)
	if req.status_code == 200 :
		content = req.json()
		for c in content['data']:
			if c[parameter] == value:
				returnDetail = c
				return returnDetail
	else :
		print "\n\nUnable to connect. Check if session is still valid\n\n"

#Reading comments of the particular post, .
def readComments(postID,pageAccessToken, commentMsg):
	comments = []
	readCommentsUrl = 'https://graph.facebook.com/v2.1/%s/comments' % postID
	params = {'access_token': pageAccessToken}
	url = "%s?%s" % (readCommentsUrl, urlencode(params))
	req = requests.get(url)
	if req.status_code == 200 :
		content = req.json()
		for r in content['data']:
			if r['message'] == commentMsg and checkCommentEligibility(r, pageAccessToken):		#deciding for which content comment auto reply is to be done.
				comments.append(r)
		return comments
	else :
		print "\n\nUnable to connect. Check if session is still valid\n\n"


#Main function Starts:
if __name__ == '__main__':
	accessToken = "EAACEdEose0cBANj5Nc0pgdB61UFdR06GlNiu6FuMyKTN9IvPr4ZB6a8zVzH2XEIP5x1Uoxm66X8u9QTPZBXrFeshlLRqEe9j9rTIYsF2Q2x9e18ZAqNEdVa3q4IliQsxFHLxGB0vTIEkzXBG7Hika88wV1ccTwPq9WlOjNqZCOddOBq8k7ymflR30jPUrR9fRT1e6EUNOAZDZD"
	parameter = "name"
	value = "Test"
	#Get Page Details.
	pageDetailUrl = 'https://graph.facebook.com/v2.1/me/accounts'
	pd = getDetails(accessToken,pageDetailUrl, parameter, value)
	pageID = pd['id']
	filterUrl = 'https://graph.facebook.com/v2.1/%s/posts' % pageID
	pageAccessToken = pd['access_token']
	#get the particular post.
	parameter = "message"
	value = "Experiment"
	fp = getDetails(pageAccessToken,filterUrl, parameter, value, pageID)
	postID = fp['id']
	#Read the comments of the particular post, find which comments need to be auto replied and take their ids.
	commentMsg = "experimentComment"
	commentInfo = readComments(postID,pageAccessToken,commentMsg)
	commentID = []
	for cID in commentInfo:
		commentID.append(cID['id'])

	#Post the automatic reply
	#postReply(commentID,pageAccessToken)
	reply = 'verified'
	for cID in commentID:
		posturl = 'https://graph.facebook.com/%s/comments?access_token=%s' % (cID, pageAccessToken)
		print "Posting for the id : %s with url %s" % (cID, posturl)
        req = requests.post(posturl, data={'message': reply})
        