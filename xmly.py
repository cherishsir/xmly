
#!coding:utf-8
#!coding:/usr/bin/python 
"""
dependency:
	you have to install  beautifulsoup4 modulex
	sudo pip install beautifulsoup4

description:
 ximalaya downloading program made by Meyou(Wuhan) --2015.4.27
 feel free to use it 

usage:
 1:just one page to download
 		python xmly.py  album_url 
 2:many pages  to download
 		python xmly.py album_url start_page_number  end_page_number


notice:
 after finishing downloading the album ,please remove the temporary json file.
"""
import urllib ,sys ,os
from urllib import urlopen
from bs4 import BeautifulSoup
import urllib2


def get_ids(filename):
	if "www"  in filename:
		fd=urllib.urlopen(filename)
	else:
		fd=open(filename)
	#print filename

	soup=BeautifulSoup(fd.read())
	newlist=soup.find("div", { "class" : "personal_body" })
	allids=newlist.get("sound_ids")
	idlist=allids.split(",")
	return idlist

def dlone(id):
	#http://www.ximalaya.com/tracks/5500449.json
	#print "in dlone "
	base="http://www.ximalaya.com/tracks/"
	url=base+str(id)+".json"
	#print url
	#fd=urllib2.urlopen(url)
	filename="./json/"+str(id)+".json"
	if not os.path.isfile(filename): 
		#cmd="wget "+url
		#os.system(cmd)
		dljson({"filename":filename,"url":url})
	fd=open(filename)
	json_paser(fd.read())

def json_paser(content):
	#print "in sjon_paser"
	import json
	myjson=json.loads(content)
	#print myjson["title"]
	#print myjson["play_path_64"]
	title= myjson["title"]+".mp3"
	mp3=myjson["play_path_64"]
 	if "mp3" not in mp3:
 		print "url is werid:",mp3

	#http://101.4.136.34:9999/fdfs.xmcdn.com/group6/M05/36/CF/wKgDg1TgOM3QGSfLATJ1WHmo2b0255.mp3
	base="http://101.4.136.34:9999/fdfs.xmcdn.com/"
	url=base+mp3
	#print url 
	import os 
	#cmd="wget "+ url+ " -O "+title+".mp3"
	#os.system(cmd)

	dlonemp3({"filename":title,"url":url})

def dllist(idlist):
	if not os.path.isdir("./json"):
		os.mkdir("json")

	for id in idlist:
		dlone(id)
def dlonemp3(mp3dict):                 #下载mp3音频文件
	filename=mp3dict["filename"]
	url=mp3dict["url"]
	if not os.path.isfile(filename):     #如果没有下载过
		print "downloading",filename
		dlafile(filename,url)
	else:
		print "already downloaded this file:"+filename
def dljson(jsondict):                 #下载mp3音频文件
	filename=jsondict["filename"]
	url=jsondict["url"]
	if not os.path.isfile(filename):     #如果没有下载过
		print "downloading",filename
		dlafile(filename,url,1024)
	else:
		print "already downloaded this file:"+filename

def dlafile(filename,url,size=1024*1024*10):
        """
        通用程序，给出文件名和url后，下载文件
        """
        #print url
        CHUNK=size
        #print url
        req=urlopen(url)
        size=int(req.info()["Content-Length"])
        ALL=size/CHUNK+1
        now=0
        #print "下载中 "+filename+"["+str(size/1000)+"KiB]"
        with open(filename,"wb") as fp:
            while True:
                condition=int(float(now)*100/ALL)
                if condition >100:
                    condition=100
                print "\033[91m\r[%"+str(condition)+"]\033[0m",
                sys.stdout.flush()
                chunk=req.read(CHUNK)
                if not chunk: break
                fp.write(chunk)
                now+=1

        print "\n"	
def dlall(url):
	idlist=get_ids(url)
	dllist(idlist)
def dlpages(urlfirst,start,end):
	"""
	 function:download many pages at one time
	 usage: python xmly.py  album_url  startnumber  endnumber
	"""
	for i in range(start,end+1):
		realurl=urlfirst+"?page="+str(i)
		print "page ",i,"is downloading..."
		dlall(str(realurl))

if __name__=="__main__":
	if len(sys.argv)==2:  #using the album website in terminal 
		url=str(sys.argv[1])
	elif len(sys.argv)==4:  #downloading many pages in termmial 
		urlfirst=str(sys.argv[1])
		start=int(sys.argv[2])
		end=int(sys.argv[3])
		dlpages(urlfirst,start,end)
		print "download pages finished"
		sys.exit(1)
	else: 					#waiting for ur input  after running the program
		url=raw_input("please input the album url> ")
	dlall(str(url))


