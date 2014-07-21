#encoding=utf-8
import os
import re
import time
import urllib
import urllib2
import codecs
import cookielib
import subprocess
import sys


loginurl = 'http://ssqzfw.xidian.edu.cn/modules/swyh/login.jsp'
loginurl_servlet = 'http://ssqzfw.xidian.edu.cn/modules/swyh/servlet/login'

cj = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
 
params = {
"account":"1303121901",
"password":"966260" 
}
# 传递参数设置

def get_captchaid():
	print "retrieving the captcha image ..."
	request=urllib2.Request(loginurl)
	response=urllib2.urlopen(request)
	html=response.read()
	imgurl=re.search('<img class="vcimg" src="(.+?)" tips=', html)
	if imgurl:
		url=imgurl.group(1)
		res=urllib.urlretrieve('http://ssqzfw.xidian.edu.cn' + url, 'vc.jpg')
		vcv=re.search('<input type="hidden" name="vcv" value="(.+?)"' ,html)
		if vcv:
			sys.stdout.write("now you can input the captcha: ")
			sys.stdout.flush()
			time.sleep(1)
			pwd = '000000'
			cmd = 'fbi -T 2 -a vc.jpg 2> /dev/null'
			subprocess.call("echo %s | sudo -S %s" % (pwd, cmd), shell=True)
			vcode = raw_input()
			params["vcode"] = vcode
			params["vcv"] = vcv.group(1)
		else:
			pass		
# 获取有图片验证码

def flowLogin():
	get_captchaid()
	data = urllib.urlencode(params).encode('unicode_escape')
	request = urllib2.Request(loginurl_servlet, data=data)
	response = urllib2.urlopen(request)
	if response.geturl() == "http://ssqzfw.xidian.edu.cn/modules/swyh/":
		#print 'login success ! '
		#print response.read()
		response = urllib2.urlopen("http://ssqzfw.xidian.edu.cn/modules/swyh/byll.jsp").read()
		match = re.findall('<td align="right">(.+?)</td>',response)
		if match:
			print
			print "\tAlready used: " + match[2] + " MB."
			print
	else:
		print 'login failed! Resulting url: ' + response.geturl()
# 请求登录

flowLogin()
