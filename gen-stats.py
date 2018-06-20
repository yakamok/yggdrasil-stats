import socket
import json
import datetime
import requests

ROOTDIR = "" #location you want the index.html file to be placed
CURRENTTIME = datetime.datetime.now()
GETPEERS = '{"request": "getPeers","keepalive":true}'
GETSESSIONS = '{"request": "getSessions","keepalive":true}'
GETSELF = '{"request":"getSelf"}'


def get_nodelist():
    data = requests.get("https://raw.githubusercontent.com/yakamok/yggdrasil-nodelist/master/nodelist")
    nodes = [x.split() for x in data.text.split('\n') if x]
    
    index_table = {}

    for x in nodes:
        index_table[x[0]] = x[1]
    return index_table


def check_nodelist(nodetable, key):
    if nodetable:
        if nodetable.get(key):
            result = '<div class="item"><span class="name">' + nodetable.get(key) + '</span>\
                    <span class="keylabel">' + key + '</span></div>'
        else:
            result = key
        return result
    else:
        return key


#create the html body
def html_alpha(ipv6_self):
    aplha = '<!DOCTYPE html>\n \
    <html>\n \
    <head>\n \
    <title>' + check_nodelist(NODELIST, ipv6_self) + '</title>\n \
    <link rel="stylesheet" type="text/css" href="style.css"/>\n \
    </head>\n \
    <body>\n \
    <div id="header">\n \
    <div id="title">' + check_nodelist(NODELIST, ipv6_self) + '</div>\n \
    </div>\n \
    <div id="wrapper">\n '
    return aplha


#end html body here
HTMLOMEGA = '</div>\n</body>\n</html>\n'


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
    NODELIST = get_nodelist()
except:
    NODELIST = None

try:
    ygg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ygg.connect(('localhost', 9001))

    #fetch peer data
    ygg.send(GETPEERS)
    getPeers_data = json.loads(ygg.recv(1024 * 6))

    #fetch session data
    ygg.send(GETSESSIONS)
    getSessions_data = json.loads(ygg.recv(1024 * 6))

    ygg.send(GETSELF)
    this_node = json.loads(ygg.recv(1024 * 6))

    #write all stats into an html filled markdown file(doesnt really need to be a markdown file,
    #just what my site pulls in by default)
    with open(ROOTDIR + "index.html", "w") as handle:
        handle.write(str(html_alpha(this_node['response']['self'].keys()[0])))
        handle.write("<h3>Connected Peers</h3>\n  ")

        #write stats for connected peers here
        for key, value in getPeers_data["response"]["peers"].iteritems():
            if value['port'] != 0:
                handle.write('<div class="peer">' + check_nodelist(NODELIST, key) + '</div>\n')
                handle.write('<div class="data">')
                handle.write('<div class="col1">Uptime: ' + str(datetime.timedelta(seconds=value['uptime'])) + '</div>\n')
                handle.write('<div class="col2"> Rx: ' + human_readable(value['bytes_recvd']) + '</div>\n')
                handle.write('<div class="col2"> Tx: ' + human_readable(value['bytes_sent']) + '</div>\n')
                handle.write('<div class="col2"> Port: ' + str(value['port']) + '</div>\n')
                handle.write('<div class="clear"></div>\n</div>\n')

        handle.write("<h3>Current Sessions</h3>\n  ")
        #write stats for current sessions
        for key, value in getSessions_data["response"]["sessions"].iteritems():
            handle.write('<div class="peer">' + check_nodelist(NODELIST, key) + '</div>\n')
            handle.write('<div class="data">')
            handle.write('<div class="col2">RX: ' + human_readable(value['bytes_recvd']) + '</div>\n')
            handle.write('<div class="col2">TX: ' + human_readable(value['bytes_sent']) + '</div>\n')
            handle.write('<div class="col2">Coords: ' + str(value['coords']) + '</div>\n')
            handle.write('<div class="clear"></div>\n</div>')

        #last updated time added here
        handle.write('<div class="updated">Last updated: ' + str(CURRENTTIME) + '</div>\n')
        handle.write('<a href="https://github.com/yakamok/yggdrasil-stats">ygg-stats</a>')
        handle.write(HTMLOMEGA + "\n")
except:
    print "something went wrong"
