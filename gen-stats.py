import socket
import string
import json
import datetime
import sys

updated = datetime.datetime.now()
getPeers = '{"request": "getPeers","keepalive":true}'
getSessions = '{"request": "getSessions"}'

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
	with open("/var/www/site/peers.md","w") as handle:
		#write stats for connected peers here
		handle.write("<h3>Connected Peers</h3>  ")
		for x in getPeers_data['response']['peers']:
			#filter out out your own node
			if getPeers_data['response']['peers'][x]['port'] != 0:
				handle.write('<div class="peer">' + x + '</div>')
				handle.write('<div class="data"><div class="col1">Uptime: ' + str(datetime.timedelta(seconds=getPeers_data['response']['peers'][x]['uptime'])) + '</div>' + \
							'<div class="col2"> RX: ' + str(((getPeers_data['response']['peers'][x]['bytes_recvd']) / 1024) / 1024) + 'MB</div>' + \
							'<div class="col3"> TX: ' + str(((getPeers_data['response']['peers'][x]['bytes_sent']) / 1024) / 1024) + 'MB</div>' + \
							'<div class="col4"> Port: ' + str(getPeers_data['response']['peers'][x]['port']) + '</div><div class="clear"></div></div>')
		handle.write("<h3>Current Sessions</h3>  ")
		#write stats for current sessions here
		for x in getSessions_data['response']['sessions']:
			handle.write('<div class="peer">' + x + '</div>')
			handle.write('<div class="data"><div class="col2">RX: ' + str(getSessions_data['response']['sessions'][x]['bytes_recvd']) + '</div>' + \
						'<div class="col2">TX: ' + str(getSessions_data['response']['sessions'][x]['bytes_sent']) + '</div>' + \
						'<div class="col2">Coords: ' + str(getSessions_data['response']['sessions'][x]['coords']) + '</div><div class="clear"></div></div>')
		#last updated time added here
		handle.write('<div class="updated">Last updated: ' + str(updated) + '</div>')

except:
	print "failed to connect to admin sockect"
