# yggdrasil-stats

![peerstats](peerstats.png)  

Yggdrasil-stats is for displaying connected peers and ongoing sessions in a pretty format.  
Yggdrasil stats will make a request to a [nodelist](https://github.com/yakamok/yggdrasil-nodelist) to check if there are domains assotiated with the ipv6 address and show it instead, you can add your own for your ipv6 address by forking the repo and making a pull request with your change(s).  
If you prefer to only make requests over yggdrasil there is a mirrored repo. To replace the github repo in the code with [yggdrasil-nodelist](http://git.h-ic.eu/yakamo/yggdrasil-nodelist/raw/master/nodelist), please take into account this updates each hour. Any change(s) you want to make please make on github this is only a mirror, any pull requests will be ignored on the mirror.  

### gen-stats.py 

Just add to crontab and run once a minute or more its up to you:  
*/1 * * * * python ygg-stats.py  

Make sure to change in the program 'root_dir = "/var/www/" ' to where you want index.html to be saved. Don't forget to save style.css in the same folder that the index.html will live.  

### ygg-stats.php

This is simpler if you have an already php friendly enviroment setup on your server, just drop ygg-stats.php into your desired location with style.css and it will work as is.  


### ToDo:

