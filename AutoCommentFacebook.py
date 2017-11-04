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
	accessToken = "EAACEdEose0cBAN9M6Px5pWWfz2KmBN6bseGU5IKZBR1mkwMXY3K3v94NY1RhCccq2HMeDm9Xi4AiZAv7axvmad8EcLbEabNyGEiiiRQ3ZB5T9E22htYFdFtulx5WoGVWHxnuIXBpHYtOzfPMp8wfOjBRGW7OzfIyGPnioTZC9VljouwnpkuZAS0ZCRZAyBAZAIleKYZBpdaHszwZDZD"
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
		time.sleep(5) 
		posturl = 'https://graph.facebook.com/%s/comments?access_token=%s' % (cID, pageAccessToken)
		print "Posting for the id : %s with url %s" % (cID, posturl)
        req = requests.post(posturl, data={'message': reply})
        print "posting done"
        if req.status_code == 200:
        	print "Successful for id %s" % cID
        else: 
        	print "failed for id %s" % cID