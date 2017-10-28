import sys
from urllib import urlencode
import requests
from urlparse import urlparse, parse_qs

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
			if r['message'] == commentMsg:		#deciding for which content comment auto reply is to be done.
				comments.append(r)
			return comments
	else :
		print "\n\nUnable to connect. Check if session is still valid\n\n"


#Main function Starts:
if __name__ == '__main__':
	accessToken = "EAACEdEose0cBAINCrX4sgM4KeEvgZBcZCA6o9yGN2iLtZBpV9aPtiXeAVhJ7O91tUwc3SXLkEyL5HLne2m6WNhUmC3j6fe39VOXTbLUkTDCyqmUuk8BlvfDNLMkMLRlrqFuRWazhw8qQVXeoF7LHjgQ4M6dQrrHFpGo8u1PrmdZA1pL4rKkYY9NOZCXNX0lrd2eoRcwBGfwZDZD"
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
        requests.post(posturl, data={'message': reply})