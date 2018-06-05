import socket
import string
import json
import datetime
import sys

root_dir = "" #location you want the index.html file to be placed
updated = datetime.datetime.now()
getPeers = '{"request": "getPeers","keepalive":true}'
getSessions = '{"request": "getSessions","keepalive":true}'
getSelf = "request":"getSelf"

#create the html body
html_body_aplha = '<!DOCTYPE html> \
					<html> \
					<head> \
					<title>' + ipv6_self + '</title> \
					<link rel="stylesheet" type="text/css" href="style.css"/> \
					</head> \
					<body> \
					<div id="header"> \
					<div id="title">' + ipv6_self + '</div> \
					</div> \
					<div id="wrapper"> '

#end html body here
html_body_omega = '</div> \
				</body> \
				</html>'

def human_readable(bnum): # make bytes readable
	data = int(bnum)
	if data >= 0 and data < 1000:
		return str(data) + "B"
	elif data >= 1000 and  data < 1000000:
		return str(data / 1000) + "KB"
	elif data >= 1000000 and data < 1000000000:
		return str(data / 1000000) + "MB"
	elif data >= 1000000000 and data < 1000000000000:
		return str(data / 1000000000) + "GB"

try:
	ygg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ygg.connect(('localhost', 9001))

	#fetch peer data
	ygg.send(getPeers)
	getPeers_data = json.loads(ygg.recv(1024 * 6))

	#fetch session data
	ygg.send(getSessions)
	getSessions_data = json.loads(ygg.recv(1024 * 6))

	#write all stats into an html filled markdown file(doesnt really need to be a markdown file, just what my site pulls in by default)
	with open(root_dir + "index.html","w") as handle:
		#write stats for connected peers here
		handle.write(html_body)
		handle.write("<h3>Connected Peers</h3>  ")
		for x in getPeers_data['response']['peers']:
			#filter out out your own node
			if getPeers_data['response']['peers'][x]['port'] != 0:
				handle.write('<div class="peer">' + x + '</div>')
				handle.write('<div class="data"><div class="col1">Uptime: ' + str(datetime.timedelta(seconds=getPeers_data['response']['peers'][x]['uptime'])) + '</div>' + \
							'<div class="col2"> RX: ' + human_readable(((getPeers_data['response']['peers'][x]['bytes_recvd']))) + '</div>' + \
							'<div class="col3"> TX: ' + human_readable(((getPeers_data['response']['peers'][x]['bytes_sent']))) + '</div>' + \
							'<div class="col4"> Port: ' + str(getPeers_data['response']['peers'][x]['port']) + '</div><div class="clear"></div></div>')
		handle.write("<h3>Current Sessions</h3>  ")
		#write stats for current sessions here
		for x in getSessions_data['response']['sessions']:
			handle.write('<div class="peer">' + x + '</div>')
			handle.write('<div class="data"><div class="col2">RX: ' + human_readable(getSessions_data['response']['sessions'][x]['bytes_recvd']) + '</div>' + \
						'<div class="col2">TX: ' + human_readable(getSessions_data['response']['sessions'][x]['bytes_sent']) + '</div>' + \
						'<div class="col2">Coords: ' + str(getSessions_data['response']['sessions'][x]['coords']) + '</div><div class="clear"></div></div>')
		#last updated time added here
		handle.write('<div class="updated">Last updated: ' + str(updated) + '</div>')
		handle.write(html_body_omega)

except:
	print "failed to connect to admin sockect"
