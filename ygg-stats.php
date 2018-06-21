<?php
$host = "127.0.0.1";
$port = 9001;

set_time_limit(2);

// please change this to http://git.h-ic.eu/yakamo/yggdrasil-nodelist/raw/master/nodelist if you want to use yggdrasil git
$git_nodelist = "https://raw.githubusercontednt.com/yakamok/yggdrasil-nodelist/master/nodelist"

//get the latest nodelist and save to file
function updateNodeList(){
	if(file_exists($git_nodelist)) {
		$raw_node_file = file_get_contents('https://raw.githubusercontent.com/yakamok/yggdrasil-nodelist/master/nodelist');
		$myfile = fopen("nodelist.txt", "w") or die("Unable to create file, please check permissions!");
		fwrite($myfile, $raw_node_file);
		fclose($myfile);
	}
}


// check file age if over 2hrs update
function check_if_update_needed(){
	if (file_exists("nodelist.txt")) {
		if (time()-filemtime("nodelist.txt") > 10) {
			updateNodeList();
		}
	}else {
		updateNodeList();
	}
}

// open file and create array
function parse_nodelist() {
	$data = array();
	$raw_nodes = explode("\n", file_get_contents("nodelist.txt"));
	foreach ($raw_nodes as &$value) {
		if ($value) {
			$tempy = explode(" ", $value);
			$data[$tempy[1]] = $tempy[0];
		}
	}
	return $data;
}

// check to see if ipv6 is in the nodelist and return an alias
function nodelist_index($key, $nodelist) {
	if (in_array($key, $nodelist)) {
		echo '<div class="item"><span class="name">' .
			array_search($key, $nodelist) . 
			'</span><span class="keylabel">' .
			$key .
			'</span></div>';
	}else {
		echo $key;
	}
}


// convert bytes to something human readable
function humanFileSize($size,$unit="") {
  if( (!$unit && $size >= 1<<30) || $unit == "GB")
    return number_format($size/(1<<30),2)."GB";
  if( (!$unit && $size >= 1<<20) || $unit == "MB")
    return number_format($size/(1<<20),2)."MB";
  if( (!$unit && $size >= 1<<10) || $unit == "KB")
    return number_format($size/(1<<10),2)."KB";
  return number_format($size)." bytes";
}


// convert seconds to human readable time
function secondsToTime($seconds) {
    $dtF = new \DateTime('@0');
    $dtT = new \DateTime("@$seconds");
    return $dtF->diff($dtT)->format('%a days, %h:%i.%s');
}


$getPeers = '{"request": "getPeers","keepalive":true}';
$getSessions = '{"request": "getSessions","keepalive":true}';
$getSelf = '{"request":"getSelf"}';

// check if nodelist.txt exists and if it needs updated or created
check_if_update_needed();
$nodelist_array = parse_nodelist();

// open socket
$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
$result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");

// getPeers request
socket_write($socket, $getPeers, strlen($getPeers)) or die("Could not send data to server\n");
$gpeers = socket_read ($socket, 8024) or die("Could not read server response\n");
// getSessions
socket_write($socket, $getSessions, strlen($getSessions)) or die("Could not send data to server\n");
$gsessions = socket_read ($socket, 8024) or die("Could not read server response\n");
// getSelf
socket_write($socket, $getSelf, strlen($getSelf)) or die("Could not send data to server\n");
$gself = socket_read ($socket, 2024) or die("Could not read server response\n");
// make sure connection is closed
socket_close($socket);

// convert to arrays
$getSelf_json_array = json_decode($gself, true);
$getSessions_json_array = json_decode($gsessions, true);
$getPeers_json_array = json_decode($gpeers, true);

?>
<!-- body of starts here -->
<!DOCTYPE html>
<html>
<head>
<title><?php echo key($getSelf_json_array{"response"}{"self"}); ?></title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
<div id="header">
	<div id="title"><?php echo nodelist_index(key($getSelf_json_array{"response"}{"self"}), $nodelist_array); ?></div>
</div>
<div id="wrapper">
<h3>Connected Peers</h3>
<?php
// getPeers display and oragnise data pretty here
foreach ($getPeers_json_array{"response"}{"peers"} as $key => $value) {
	if ($value{"port"}) {
		echo '<div class="peer">' . nodelist_index($key, $nodelist_array) . '</div>';
		echo '<div class="data"><div class="col1">' . secondsToTime((int)$value{"uptime"}) . '</div>';
		echo '<div class="col2">Rx: ' . humanFileSize($value{"bytes_recvd"}) . '</div>';
		echo '<div class="col2">Tx: ' . humanFileSize($value{"bytes_sent"}). '</div>';
		echo '<div class="col2">Port: ' . $value{"port"} . '</div>';
		echo '<div class="clear"></div></div>';
	}
}
echo '<h3>Current Sessions</h3>';
// getSessions display and oragnise data pretty here
foreach ($getSessions_json_array{"response"}{"sessions"} as $key => $value) {
	echo '<div class="peer">' . nodelist_index($key, $nodelist_array) . '</div>';
	echo '<div class="data">';
	echo '<div class="col2">Rx: ' . humanFileSize($value{"bytes_recvd"}) . '</div>';
	echo '<div class="col2">Tx: ' . humanFileSize($value{"bytes_sent"}) . '</div>';
	echo '<div class="col2">Coords: ' . $value{"coords"} . '</div>';
	echo '<div class="clear"></div></div>';
}
?>
<div class="updated">Last updated: <?php echo date("Y-m-d H:i:s"); ?> </div>
<br />
<a href="https://github.com/yakamok/yggdrasil-stats">ygg-stats</a>
</div>
</body>
</html>
