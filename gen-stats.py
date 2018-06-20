import socket
import json
import datetime

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
html_body_omega = '</div>\n</body>\n</html>\n'

def human_readable(bnum): # make bytes readable
    data = int(bnum)
    if data >= 0 and data < 1000:
        result = str(data) + "B"
    elif data >= 1000 and  data < 1000000:
        result = str(data / 1000) + "KB"
    elif data >= 1000000 and data < 1000000000:
        result = str(data / 1000000) + "MB"
    elif data >= 1000000000 and data < 1000000000000:
        result = str(data / 1000000000) + "GB"
    return result

try:
    ygg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ygg.connect(('localhost', 9001)
                
  
  #fetch peer data
    ygg.send(getPeers)
    getPeers_data = json.loads(ygg.recv(1024 * 8))

  #fetch session data
    ygg.send(getSessions)
    getSessions_data = json.loads(ygg.recv(1024 * 8))

    ygg.send(getSelf)
    this_node = json.loads(ygg.recv(1024 * 2))
    print this_node['response']['self'].keys()[0]

    #write to index.html
    with open(root_dir + "index.html", "w") as handle:
        handle.write(str(html_body_alpha(this_node['response']['self'].keys()[0])))
        handle.write("<h3>Connected Peers</h3>\n  ")

    #write stats for connected peers here
    for key, value in getPeers_data["response"]["peers"].iteritems():
        if value['port'] != 0:
            handle.write('<div class="peer">' + key + '</div>\n')
            handle.write('<div class="data">')
            handle.write('<div class="col1">Uptime: ' + str(datetime.timedelta(seconds=value['uptime'])) + '</div>\n')
            handle.write('<div class="col2"> Rx: ' + human_readable(value['bytes_recvd']) + '</div>\n')
            handle.write('<div class="col2"> Tx: ' + human_readable(value['bytes_sent']) + '</div>\n')
            handle.write('<div class="col2"> Port: ' + str(value['port']) + '</div>\n')
            handle.write('<div class="clear"></div>\n</div>\n')

    handle.write("<h3>Current Sessions</h3>\n  ")
    #write stats for current sessions
    for key, value in getSessions_data["response"]["sessions"].iteritems():
        handle.write('<div class="peer">' + key + '</div>\n')
        handle.write('<div class="data">')
        handle.write('<div class="col2">RX: ' + human_readable(value['bytes_recvd']) + '</div>\n')
        handle.write('<div class="col2">TX: ' + human_readable(value['bytes_sent']) + '</div>\n')
        handle.write('<div class="col2">Coords: ' + str(value['coords']) + '</div>\n')
        handle.write('<div class="clear"></div>\n</div>')

    #last updated time added here
    handle.write('<div class="updated">Last updated: ' + str(updated) + '</div>\n')
    handle.write('<a href="https://github.com/yakamok/yggdrasil-stats">ygg-stats</a>')
    handle.write(html_body_omega + "\n")
except:
    print "failed to connect to admin sockect"
