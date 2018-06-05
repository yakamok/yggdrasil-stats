import socket
import string
import json
import datetime
import sys

root_dir = "" #location you want the index.html file to be placed
updated = datetime.datetime.now()
getPeers = '{"request": "getPeers","keepalive":true}'
getSessions = '{"request": "getSessions","keepalive":true}'
getSelf = '{"request":"getSelf"}'

#create the html body
def html_body_alpha(ipv6_self):
  aplha = '<!DOCTYPE html>\n \
  <html>\n \
  <head>\n \
  <title>' + ipv6_self + '</title>\n \
  <link rel="stylesheet" type="text/css" href="style.css"/>\n \
  </head>\n \
  <body>\n \
  <div id="header">\n \
  <div id="title">' + ipv6_self + '</div>\n \
  </div>\n \
  <div id="wrapper">\n '
  return aplha

#end html body here
html_body_omega = '</div>\n \
        </body>\n \
        </html>\n'

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

	ygg.send(getSelf)
	this_node = json.loads(ygg.recv(1024 * 6))
	print this_node['response']['self'].keys()[0]
	#write all stats into an html filled markdown file(doesnt really need to be a markdown file, just what my site pulls in by default)
	with open(root_dir + "index.html","w") as handle:
	  #write stats for connected peers here
	  handle.write(str(html_body_alpha(this_node['response']['self'].keys()[0])))
	  handle.write("<h3>Connected Peers</h3>\n  ")
	  for x in getPeers_data['response']['peers']:
	    #filter out out your own node
	    if getPeers_data['response']['peers'][x]['port'] != 0:
	      handle.write('<div class="peer">' + x + '</div>\n')
	      handle.write('<div class="data"><div class="col1">Uptime: ' + str(datetime.timedelta(seconds=getPeers_data['response']['peers'][x]['uptime'])) + '</div>\n' + \
		    '<div class="col2"> Rx: ' + human_readable(((getPeers_data['response']['peers'][x]['bytes_recvd']))) + '</div>\n' + \
		    '<div class="col3"> Tx: ' + human_readable(((getPeers_data['response']['peers'][x]['bytes_sent']))) + '</div>\n' + \
		    '<div class="col4"> Port: ' + str(getPeers_data['response']['peers'][x]['port']) + '</div>\n<div class="clear"></div>\n</div>\n')
	  handle.write("<h3>Current Sessions</h3>\n  ")
	  #write stats for current sessions here
	  for x in getSessions_data['response']['sessions']:
	    handle.write('<div class="peer">' + x + '</div>\n')
	    handle.write('<div class="data"><div class="col2">\nRX: ' + human_readable(getSessions_data['response']['sessions'][x]['bytes_recvd']) + '</div>\n' + \
		  '<div class="col2">TX: ' + human_readable(getSessions_data['response']['sessions'][x]['bytes_sent']) + '</div>\n' + \
		  '<div class="col2">Coords: ' + str(getSessions_data['response']['sessions'][x]['coords']) + '</div>\n<div class="clear"></div>\n</div>')
	  #last updated time added here
	  handle.write('<div class="updated">Last updated: ' + str(updated) + '</div>\n')
	  handle.write(html_body_omega + "\n")

except:
  print "failed to connect to admin sockect"
