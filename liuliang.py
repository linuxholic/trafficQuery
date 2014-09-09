#encoding=utf-8
import re
import urllib
import urllib2
import cookielib
import subprocess
import sys
import time
from PIL import Image
from pytesser import *

# hardcode some urls
login_captcha = 'http://ssqzfw.xidian.edu.cn/modules/swyh/login.jsp'
login_post = 'http://ssqzfw.xidian.edu.cn/modules/swyh/servlet/login'
host = 'http://ssqzfw.xidian.edu.cn'
login_success_page = "http://ssqzfw.xidian.edu.cn/modules/swyh/"
detail_page = "http://ssqzfw.xidian.edu.cn/modules/swyh/byll.jsp"

# handle cookie
cj = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# form data to POST
params = {
"account":"1303121901",
"password":"966260" 
}

# invoke tiv to show the captcha image within terminal
def show_captcha():
	print
	print
	subprocess.call(['tiv','-w','80', 'vc.jpg']) 
	print


# add form data for POST
def fill_params(html):
	vcv=re.search('<input type="hidden" name="vcv" value="(.+?)"' ,html)
	if vcv:
		#vcode = raw_input('Now you need to input the above captcha: ')
		vcode = image_file_to_string('vc.jpg')
		params["vcode"] = vcode
		params["vcv"] = vcv.group(1)
	else:
		print 'field vcv not found!'		

def get_captcha():
	print
	sys.stdout.write("retrieving the captcha image ...")
	sys.stdout.flush()
	response = urllib2.urlopen(login_captcha)
	html = response.read()
	imgurl = re.search('<img class="vcimg" src="(.+?)" tips=', html)
	if imgurl:
		url = imgurl.group(1)
		res = urllib.urlretrieve( host + url, 'vc.jpg')
		show_captcha()
		fill_params(html)
	else:
		print 'Failed to retrieve captcha!'

def netFlow():
	get_captcha()
	data = urllib.urlencode(params)
	request = urllib2.Request(login_post, data=data)
	response = urllib2.urlopen(request)
	if response.geturl() == login_success_page:
		response = urllib2.urlopen(detail_page).read()
		match = re.findall('<td align="right">(.+?)</td>',response)
		if match:
			print
			print "\tAlready used: " + match[2] + " MB."
			print
	else:
		print 'login failed! Resulting url: ' + response.geturl()
		time.sleep(1)
		netFlow()

netFlow()
