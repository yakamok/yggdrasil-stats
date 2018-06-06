# yggdrasil-stats

![peerstats](peerstats.png)

This small program collects stats from yggdrasil admin api and turns it into html.  

Just add to crontab and run once a minute or more its up to you:  
*/1 * * * * python ygg-stats.py  

Make sure to change in the program 'root_dir = "" ' to where you want index.html to be saved along with style.css.  

### ToDo:

Clean up code  
